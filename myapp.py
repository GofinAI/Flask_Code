from flask import Flask, render_template, request, redirect, url_for,send_file
from flask_mysqldb import MySQL
import mysql.connector as db
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'gofin-aurora-instance-1.ci0rkg2zgzsd.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'malikam'
app.config['MYSQL_PASSWORD'] = 'Malika@98966'
app.config['MYSQL_DB'] = 'usda'

mydb = MySQL(app)

GD,CD,SD,UD,PP,CDesc,State,FD,PD,table = "","","","","","","","","",""
gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d, final_d = "","","","","","","","",""

@app.route("/")
@app.route("/home")
def home():
    global gd_d
    cursor = mydb.connection.cursor()
    cursor.execute("SELECT * FROM S_GROUP_DESC")
    gd_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html",gd_data = gd_d)

@app.route("/group_description")
def group_description():
    global GD
    global gd_d, cd_d
    GD = request.args.get("GD")
    cursor = mydb.connection.cursor()
    cursor.execute("""SELECT CROPS FROM S_CROPS where GROUP_DESC = %s order by CROPS""",(GD,))
    cd_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", cd_data =cd_d,gd_data = gd_d)

@app.route("/commodity_desc")
def commodity_desc():
    global GD,CD
    global gd_d, cd_d, sd_d
    #print(GD)
    CD = request.args.get("CD")
    #print(CD)
    cursor = mydb.connection.cursor()
    cursor.execute("""SELECT STATISTICCAT_DESC FROM S_STATISTICCAT_DESC where 
                    GROUP_DESC = %s and CROPS = %s order by STATISTICCAT_DESC""",(GD,CD))
    sd_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route("/statisticcat_desc")
def statisticcat_desc():
    global GD,CD,SD
    global gd_d, cd_d, sd_d, ud_d

    SD = request.args.get("SD")
    cursor = mydb.connection.cursor()
    cursor.execute("""SELECT UNIT_DESC FROM S_UNIT_DESC where 
                    GROUP_DESC = %s and CROPS = %s and STATISTICCAT_DESC = %s""",(GD,CD,SD))
    ud_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route("/unit_desc")
def unit_desc():
    global GD,CD,SD,UD
    global gd_d, cd_d, sd_d, ud_d, pp_d

    UD = request.args.get("UD")
    cursor = mydb.connection.cursor()
    cursor.execute("""SELECT PRODUCTION_PRACTICE FROM usda.S_PROD_PRACTICE 
                    where 
                    GROUP_DESC = %s and CROPS = %s and STATISTICCAT_DESC = %s and UNIT_DESC = %s
                    order by PRODUCTION_PRACTICE""",(GD,CD,SD,UD))
    pp_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)
    
@app.route("/production_prac")
def production_prac():
    global GD,CD,SD,UD,PP
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d

    PP = request.args.get("PP")
    cursor = mydb.connection.cursor()
    cursor.execute("""SELECT CLASS_DESC FROM usda.S_CLASS_DESC where GROUP_DESC = %s and CROPS = %s and STATISTICCAT_DESC = %s 
                      and UNIT_DESC = %s and PRODUCTION_PRACTICE = %s order by PRODUCTION_PRACTICE""",(GD,CD,SD,UD,PP))
    cdesc_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)   

@app.route("/class_desc")
def class_desc():
    global GD,CD,SD,UD,PP,CDesc
    
    CDesc = request.args.get("CDesc")
    return render_template("Request.html",cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)    

@app.route("/States")
def States():
    global GD,CD,SD,UD,PP,CDesc,State,table
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d

    State = request.args.get("States")
    cursor = mydb.connection.cursor()
   
    if(State == 'US TOTAL'):
        if(GD == 'VEGETABLES'):
            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_VEGETABLE_US_DETAILS 
                           WHERE 
                           CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD)

            table = "S_VEGETABLE_US_DETAILS"

        elif(GD == 'HORTICULTURE'):
            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_HORTICULTURE_US_DETAILS
                            WHERE 
                            CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)
            
            table = "S_HORTICULTURE_US_DETAILS"

        elif(GD == 'FIELD CROPS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_FIELD_CROPS_US_DETAILS
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_FIELD_CROPS_US_DETAILS"

        elif(GD == 'FRUIT & TREE NUTS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_FRUIT_AND_TREE_NUTS_US_DETAILS
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_FRUIT_AND_TREE_NUTS_US_DETAILS"

        elif(GD == 'CROP TOTALS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_CROP_TOTALS_US_DETAILS
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_CROP_TOTALS_US_DETAILS"

        elif(GD == 'COMMODITIES'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_COMMODITIES_US_DETAILS 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_COMMODITIES_US_DETAILS"    

#OTHER STATES        
    else:
        if(GD == 'VEGETABLES'):
            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_VEGETABLE_STATE_DETAILS 
                            WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_VEGETABLE_STATE_DETAILS"

        elif(GD == 'HORTICULTURE'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_HORTICULTURE_STATE_DETAILS 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_HORTICULTURE_STATE_DETAILS"

        elif(GD == 'FIELD CROPS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_FIELD_CROPS_STATE_DETAILS 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_FIELD_CROPS_STATE_DETAILS"

        elif(GD == 'FRUIT & TREE NUTS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_FRUIT_AND_TREE_NUTS_STATE_DETAILS 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_FRUIT_AND_TREE_NUTS_STATE_DETAILS"

        elif(GD == 'CROP TOTALS'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_CROP_TOTALS_STATE_DETAILS 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_CROP_TOTALS_STATE_DETAI"

        elif(GD == 'COMMODITIES'):

            sql_query = """SELECT Distinct FREQ_DESC FROM usda.S_COMMODITIES_STATE_DETAILS; 
                        WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and `{}` IS NOT NULL """.format(SD,SD)

            table = "S_COMMODITIES_STATE_DETAILS"
            
    cursor.execute(sql_query, (CD, PP,UD,CDesc))
    fd_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", fd_data = fd_d, cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route('/freq_desc')
def freq_desc():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d
    
    FD = request.args.get("FD")
    cursor = mydb.connection.cursor()
    cursor.execute("""Select Distinct PERIOD_REFERENCE from `{}` 
            WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and FREQ_DESC = %s order by STATE_NAME""".format(table),(CD, PP,UD,CDesc,FD))
    pd_d = cursor.fetchall()
    cursor.close()
    return render_template("Request.html", pd_data = pd_d, fd_data = fd_d, cdesc_data = cd_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route('/period_ref')
def period_ref():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD,PD
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d, final_d

    PD = request.args.get("PD")
    cursor = mydb.connection.cursor()
    cursor.execute("""Select CROP_TYPE, PRODUCTION_PRACTICE, YEAR, PERIOD_REFERENCE, STATE_NAME, `{}`, CLASS_DESC 
                    from `{}` 
                    WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and FREQ_DESC = %s and PERIOD_REFERENCE = %s and `{}` IS NOT NULL """.format(SD,table,SD),(CD, PP,UD,CDesc,FD,PD))

    columns = [description[0] for description in cursor.description]
    final_d = cursor.fetchall()
    return render_template("Request.html", data = final_d, pd_data = pd_d, fd_data = fd_d, cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d,columns=columns)

@app.route('/plot', methods=['POST'])
def plot_post():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD,PD
    
    xaxis = request.form['xaxis']
    yaxis = request.form['yaxis']
    cursor = mydb.connection.cursor()
    query = """Select `{}`, `{}` from `{}` 
                    WHERE CROP_TYPE = %s AND PRODUCTION_PRACTICE = %s and UNIT_DESC = %s and CLASS_DESC = %s and FREQ_DESC = %s and PERIOD_REFERENCE = %s and `{}` IS NOT NULL """.format(xaxis,yaxis,table,SD)
    cursor.execute(query, (CD, PP,UD,CDesc,FD,PD))
    columns = [description[0] for description in cursor.description]
    result = cursor.fetchall()
    # Do something with xaxis and yaxis here
    X=[]
    Y=[]
    for row in result:
        X.append(row[0])
        Y.append(row[1])

    with sns.axes_style('darkgrid'):
        plt.figure(figsize=(15, 5))
        plt.plot(X,Y,c="mediumseagreen",linewidth = 2.5)
        # Plot Labels

        plt.xlabel(xaxis, fontsize=15, color='blue',fontweight='bold')
        plt.ylabel(yaxis,fontsize=15, color='blue',fontweight='bold')

        # Plot Ticks

        plt.xticks(X,fontsize=15,rotation=30)
        plt.yticks(fontsize=15)
        plt.margins(0.1)
        plt.tick_params(axis='x',  pad =8)
        plt.locator_params(axis='x', nbins=10)
        plt.locator_params(axis='y', nbins=10)

        plt.grid(color ='grey', linestyle ='-.', linewidth = 1, alpha = 0.2)

        font = {'family': 'serif',
                'color':  'darkred',
                'weight': 'bold',
                'size': 12,
                }

        for index in range(len(X)):
            plt.text(X[index], Y[index], Y[index],horizontalalignment='center',
        verticalalignment='center', fontdict=font)

        font1 = {'family': 'serif',
                'color':  'darkred',
                'weight': 'normal',
                'size': 12,
                }

        text = (GD + "\n" + CD + "\n" + SD + "\n" + UD + "\n" + PP
                + "\n" + State )

        plt.text(X[index]+0.8, max(Y), text,horizontalalignment='left',verticalalignment='center', fontdict=font1,
                 bbox=dict(boxstyle = "square",
                      facecolor = "whitesmoke"))
        plt.savefig('static/plot.png')  # Save the plot image
        return render_template('plot.html')

if __name__ =='__main__':
    app.run()
    