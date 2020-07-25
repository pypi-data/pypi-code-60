"""Count balls using an entrance switch."""
import asyncio

from mpf.devices.ball_device.physical_ball_counter import PhysicalBallCounter, BallEntranceActivity, \
    BallLostActivity


class EntranceSwitchCounter(PhysicalBallCounter):

    """Count balls using an entrance switch."""

    __slots__ = ["recycle_secs", "recycle_clear_time"]

    def __init__(self, ball_device, config):
        """Initialise entrance switch counter."""
        super().__init__(ball_device, config)

        self.recycle_secs = self.config['entrance_switch_ignore_window_ms'] / 1000.0
        self.recycle_clear_time = {}

        for switch in self.config['entrance_switch']:
            # Configure switch handlers for entrance switch activity
            self.machine.switch_controller.add_switch_handler_obj(
                switch=switch, state=1,
                ms=0,
                callback=self._entrance_switch_handler,
                callback_kwargs={"switch_name": switch.name})

        if self.config['entrance_switch_full_timeout'] and self.config['ball_capacity']:
            if len(self.config['entrance_switch']) > 1:
                raise AssertionError("entrance_switch_full_timeout not supported with multiple entrance switches.")
            self.machine.switch_controller.add_switch_handler_obj(
                switch=self.config['entrance_switch'][0], state=1,
                ms=self.config['entrance_switch_full_timeout'],
                callback=self._entrance_switch_full_handler)

        # Handle initial ball count with entrance_switch. If there is a ball on the entrance_switch at boot
        # assume that we are at max capacity.
        if (self.config['ball_capacity'] and self.config['entrance_switch_full_timeout'] and
                self.machine.switch_controller.is_active(self.config['entrance_switch'][0],
                                                         ms=self.config['entrance_switch_full_timeout'])):
            self._last_count = self.config['ball_capacity']
        else:
            self._last_count = 0
        self._count_stable.set()

    def is_jammed(self) -> bool:
        """Return False because this device can not know if it is jammed."""
        return False

    def is_count_unreliable(self) -> bool:
        """Return False because this device can not know if it is jammed."""
        return False

    def received_entrance_event(self):
        """Handle entrance event."""
        self._entrance_switch_handler("event")

    def _recycle_passed(self, switch):
        self.recycle_clear_time[switch] = None

    def _entrance_switch_handler(self, switch_name):
        """Add a ball to the device since the entrance switch has been hit."""
        # If recycle is ongoing, do nothing
        if self.recycle_clear_time.get(switch_name, False):
            self.debug_log("Entrance switch hit within ignore window, taking no action")
            return
        # If a recycle time is configured, set a timeout to prevent future entrance activity
        if self.recycle_secs:
            self.recycle_clear_time[switch_name] = self.machine.clock.get_time() + self.recycle_secs
            self.machine.clock.loop.call_at(self.recycle_clear_time[switch_name], self._recycle_passed, switch_name)

        self.debug_log("Entrance switch hit")
        if self.config['ball_capacity'] and self.config['ball_capacity'] <= self._last_count:
            # do not count beyond capacity
            self.ball_device.log.warning("Device received balls but is already full!")
        elif self.config['ball_capacity'] and self.config['entrance_switch_full_timeout'] and \
                self.config['ball_capacity'] == self._last_count + 1:
            # wait for entrance_switch_full_timeout before setting the device to full capacity
            self.invalidate_count()
        else:
            # increase count
            self._last_count += 1
            self._count_stable.set()
            self.trigger_activity()
            self.record_activity(BallEntranceActivity())

    def _entrance_switch_full_handler(self):
        # a ball is sitting on the entrance_switch. assume the device is full
        new_balls = self.config['ball_capacity'] - self._last_count
        self._count_stable.set()
        self.trigger_activity()
        if new_balls > 0:
            self.debug_log("Ball is sitting on entrance_switch. Assuming "
                           "device is full. Adding %s balls and setting balls"
                           "to %s", new_balls, self.config['ball_capacity'])
            self._last_count += new_balls
            for _ in range(new_balls):
                self.record_activity(BallEntranceActivity())

    def count_balls_sync(self) -> int:
        """Return the number of balls entered."""
        if self.config['ball_capacity'] and self.config['ball_capacity'] == self._last_count:
            # we are at capacity. this is fine
            pass
        elif self.config['ball_capacity'] and self.config['entrance_switch_full_timeout'] and \
            self.config['ball_capacity'] == self._last_count + 1 and \
            self.machine.switch_controller.is_active(self.config['entrance_switch'][0],
                                                     ms=self.config['entrance_switch_full_timeout']):
            # can count when entrance switch is active for at least entrance_switch_full_timeout
            pass
        elif not self.is_ready_to_receive:
            # cannot count when the entrance_switch is still active
            raise ValueError

        return self._last_count

    async def wait_for_ball_to_leave(self):
        """Wait for a ball to leave."""
        await self.wait_for_count_stable()
        # wait 10ms
        done_future = asyncio.ensure_future(asyncio.sleep(0.01, loop=self.machine.clock.loop),
                                            loop=self.machine.clock.loop)
        done_future.add_done_callback(self._ball_left)
        return done_future

    def _ball_left(self, future):
        del future
        self._last_count -= 1
        self.record_activity(BallLostActivity())
        self.trigger_activity()

    @property
    def is_ready_to_receive(self):
        """Return true if entrance switch is inactive."""
        return not all(self.machine.switch_controller.is_active(switch) for switch in self.config['entrance_switch'])

    async def wait_for_ready_to_receive(self):
        """Wait until all entrance switch are inactive."""
        while True:
            if self.is_ready_to_receive:
                return True

            await self.machine.switch_controller.wait_for_any_switch(
                switches=self.config['entrance_switch'],
                state=0, only_on_change=True)
