import pandas as pd


def multi_table_style(df_list, index: False):
    """ Apply a default clean table style to pandas df.to_html() for use in email strings.
    This version returns multiple tables stacked on top of each other with a line break inbetween.

    :param index: Determines whether you want index displayed in the HTML. Defaults to False.
    :type index: Boolean
    :param df_list: List of dataframes to return in html format.
    :type df: Pandas Dataframe
    :return: HTML string for insertion in email.
    :rtype: string
    """
    if index:
        html_string = (
            """
                <head>
                    <style>
                        table.dataframe {
                            border-collapse: collapse;
                        }
                        table.dataframe th{
                            border: 1px solid black;
                            padding: 10px;
                            font-size:14px;
                            text-align: center;
                        }
                        table.dataframe td {
                            border: 1px solid black;
                            padding: 10px;
                            font-size:12px;
                            text-align: center;
                        }
                    }
                    </style>
                </head>
                """
        )
        for i in df_list:
            html_string = html_string + i.to_html() + "<br/> <br/>"
    else:
        html_string = (
            """
                <head>
                    <style>
                        table.dataframe {
                            border-collapse: collapse;
                        }
                        table.dataframe th{
                            border: 1px solid black;
                            padding: 10px;
                            font-size:14px;
                            text-align: center;
                        }
                        table.dataframe td {
                            border: 1px solid black;
                            padding: 10px;
                            font-size:12px;
                            text-align: center;
                        }
                    }
                    </style>
                </head>
                """
        )
        for i in df_list:
            html_string = html_string + i.to_html(index=False) + "<br/> <br/>"

    return html_string
