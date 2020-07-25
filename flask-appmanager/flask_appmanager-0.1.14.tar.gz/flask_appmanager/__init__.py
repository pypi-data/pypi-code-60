from flask import *
import os,sys,logging
from os import path
from werkzeug.utils import secure_filename
import linecache
from pypinyin import lazy_pinyin
def Appexcepthook(exc_type, exc_value, tb):
	count=0
	msg = ''
	while tb:
		count+=1
		filename = tb.tb_frame.f_code.co_filename
		name = tb.tb_frame.f_code.co_name
		lineno = tb.tb_lineno
		msg += '	文件 "%.500s", 第 %d 行, 在 %.500s\n' % (filename, lineno, name)
		msg+=  '		行内容：'+linecache.getline(filename,lineno)
		tb = tb.tb_next

	msg += '[错误名称] %s: %s\n' %(exc_type.__name__, exc_value)
	msg2='[报错提示] Flask App-Manager为您抓获%d个异常：\n'%count+msg
	print(msg2)
# sys.excepthook=Appexcepthook
manager=Blueprint('manager',__name__,template_folder='manager_template',static_folder='manager_static')

manager.app=None
MANAGER_MDUI_CDN='''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mdui/0.4.3/css/mdui.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/mdui/0.4.3/js/mdui.min.js"></script>'''

@manager.before_request
def before():

	if session.get('manage_user')==None:
		if request.path!=url_for('.login')and request.path!=url_for('.login_verify'):return redirect(url_for('.login'))
		else:return
	else:
		return



@manager.route('/')
def manager_index():
	rules=[]
	app=manager.app
	for i in (app.url_map._rules_by_endpoint):
		r=[str(x) for x in app.url_map._rules_by_endpoint[i]]
		rules.append('''<li class="mdui-list-item mdui-ripple"><div class="mdui-list-item-content">路由路径（可能存在多个）：{}<br>路由连接函数名：{}</div></li><div class="mdui-divider-inset mdui-m-y-0"></div>'''.format(escape('，'.join(r)) ,escape(i.replace('.','->'))))
	return render_template('manager_template.html',mdui_cdn=MANAGER_MDUI_CDN,content='''
<div class="mdui-typo">
<h1>概览</h1><hr><h3>路由列表</h3>
		<ul class="mdui-list mdui-list-dense">
{}
</ul></div>'''.format(''.join(rules)))

@manager.route('/login')
def login():
	return render_template('manager_login.html',mdui_cdn=MANAGER_MDUI_CDN)

@manager.route('/verify',methods=['GET','POST'])
def login_verify():
	name=request.form.get('username')
	psw=request.form.get('psw')
	# print(name,psw)
	if name=='admin' and psw=='12345':
		session['manage_user']=name+'|'+psw
		return redirect(url_for('.manager_index'))
	else:
		return redirect(url_for('.login'))

@manager.route("/upload",methods=['POST'])
def upload():
	
	if request.method=='POST':
		try:
			f = request.files["file"]
			if not f:return '请上传文件！'
			base_path = path.abspath(path.dirname(__name__))
			upload_path = path.join(base_path,manager.astatic,secure_filename(''.join(lazy_pinyin(f.filename))))
			
			f.save(upload_path)
			return redirect(url_for('.staticUpload'))
		except FileNotFoundError:
			return '找不到静态资源目录，请检查拼写或查看该目录是否存在'


@manager.route("/static",methods=['GET'])
def staticUpload():
	l=['<a class="mdui-list-item mdui-ripple" href="{}">{}</a>'.format(url_for('static',filename=i),i) for i in os.listdir(manager.astatic)]
	return render_template('manager_template.html',mdui_cdn=MANAGER_MDUI_CDN,content='''<div class="mdui-typo"><h1>上传文件到static</h1><hr><form action="{}" method="post" enctype="multipart/form-data">
		<input type="file" name="file" require="" >

		<input type="submit" value="上传" class="mdui-btn mdui-color-light-blue">
	</form>
	<h3>文件列表</h3><hr></div>
		<div class="mdui-list">
		{}
		</div>


	'''.format(url_for('.upload'),''.join(l)))



def manage_app(app,upload_static_folder):
	manager.astatic=upload_static_folder
	manager.app=app
	app.register_blueprint(manager,url_prefix='/manager')

