from flask import Flask, render_template, request
import mysql.connector as db
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

mydb = db.connect(
    host = "gofin-aurora-instance-1.ci0rkg2zgzsd.us-east-1.rds.amazonaws.com",
    user = "malikam",
    password = "Malika@98966",
    database = "usda"
)
if mydb:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")
mycursor = mydb.cursor()

GD,CD,SD,UD,PP,CDesc,State,FD,PD,table = "","","","","","","","","",""
gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d, final_d = "","","","","","","","",""

@app.route("/")
@app.route("/home")
def home():
    global gd_d
    cursor = mydb.cursor()
    cursor.callproc("S_GROUP_DESC_SP")
    for result in cursor.stored_results():
        gd_d = result.fetchall()
    cursor.close()
    return render_template("Request.html",gd_data = gd_d)

@app.route("/group_description")
def group_description():
    global GD
    global gd_d, cd_d
    GD = request.args.get("GD")
    cursor = mydb.cursor()
    cursor.callproc("S_CROPS_SP",(GD,))
    for result in cursor.stored_results():
        cd_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", cd_data =cd_d,gd_data = gd_d)

@app.route("/commodity_desc")
def commodity_desc():
    global GD,CD
    global gd_d, cd_d, sd_d
    #print(GD)
    CD = request.args.get("CD")
    #print(CD)
    cursor = mydb.cursor()
    cursor.callproc("S_STATISTICCAT_DESC_SP",(GD,CD))
    for result in cursor.stored_results():
        sd_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route("/statisticcat_desc")
def statisticcat_desc():
    global GD,CD,SD
    global gd_d, cd_d, sd_d, ud_d

    SD = request.args.get("SD")
    cursor = mydb.cursor()
    cursor.callproc("S_UNIT_DESC_SP",(GD,CD,SD))
    for result in cursor.stored_results():
        ud_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route("/unit_desc")
def unit_desc():
    global GD,CD,SD,UD
    global gd_d, cd_d, sd_d, ud_d, pp_d

    UD = request.args.get("UD")
    cursor = mydb.cursor()
    cursor.callproc("S_PROD_PRACTICE_SP",(GD,CD,SD,UD))
    for result in cursor.stored_results():
        pp_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)
    
@app.route("/production_prac")
def production_prac():
    global GD,CD,SD,UD,PP
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d

    PP = request.args.get("PP")
    cursor = mydb.cursor()
    cursor.callproc("S_CLASS_DESC_SP",(GD,CD,SD,UD,PP))
    for result in cursor.stored_results():
        cdesc_d = result.fetchall()
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
    cursor = mydb.cursor()
   
    if(State == 'US TOTAL'):
        if(GD == 'VEGETABLES'):
            table = "S_VEGETABLE_US_DETAILS"

        elif(GD == 'HORTICULTURE'):
            table = "S_HORTICULTURE_US_DETAILS"

        elif(GD == 'FIELD CROPS'):
            table = "S_FIELD_CROPS_US_DETAILS"

        elif(GD == 'FRUIT & TREE NUTS'):
            table = "S_FRUIT_AND_TREE_NUTS_US_DETAILS"

        elif(GD == 'CROP TOTALS'):
            table = "S_CROP_TOTALS_US_DETAILS"

        elif(GD == 'COMMODITIES'):
            table = "S_COMMODITIES_US_DETAILS"    

#OTHER STATES        
    else:
        if(GD == 'VEGETABLES'):
            table = "S_VEGETABLE_STATE_DETAILS"

        elif(GD == 'HORTICULTURE'):
            table = "S_HORTICULTURE_STATE_DETAILS"

        elif(GD == 'FIELD CROPS'):
            table = "S_FIELD_CROPS_STATE_DETAILS"

        elif(GD == 'FRUIT & TREE NUTS'):
            table = "S_FRUIT_AND_TREE_NUTS_STATE_DETAILS"

        elif(GD == 'CROP TOTALS'):
            table = "S_CROP_TOTALS_STATE_DETAI"

        elif(GD == 'COMMODITIES'):
            table = "S_COMMODITIES_STATE_DETAILS"
            
    sql_query = "FREQ_DESC_SP"
    cursor.callproc(sql_query, (table,CD, PP,UD,CDesc,SD))
    for result in cursor.stored_results():
        fd_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", fd_data = fd_d, cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route('/freq_desc')
def freq_desc():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d
    
    FD = request.args.get("FD")
    cursor = mydb.cursor()
    cursor.callproc("PERIOD_REFERENCE_SP",(table,CD, PP,UD,CDesc,SD,FD))
    for result in cursor.stored_results():
        pd_d = result.fetchall()
    cursor.close()
    return render_template("Request.html", pd_data = pd_d, fd_data = fd_d, cdesc_data = cd_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route('/period_ref')
def period_ref():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD,PD
    global gd_d, cd_d, sd_d, ud_d, pp_d, cdesc_d, fd_d,pd_d,final_d

    PD = request.args.get("PD")
    cursor = mydb.cursor()
    cursor.callproc("CROP_DETAILS_SP",(table,CD, PP,UD,CDesc,SD,FD,PD))
    for result in cursor.stored_results():
        final_d = result.fetchall()   
    cursor.close()     

    return render_template("Request.html", pd_data = pd_d, fd_data = fd_d, cdesc_data = cdesc_d, pp_data = pp_d, ud_data = ud_d, sd_data = sd_d,cd_data =cd_d,gd_data = gd_d)

@app.route('/plot', methods=['POST'])
def plot_post():
    global GD,CD,SD,UD,PP,CDesc,State,table,FD,PD,final_d
    
    columns = ["CROP_TYPE", "PRODUCTION_PRACTICE", "YEAR", "PERIOD_REFERENCE", "STATE_NAME",SD,"CLASS_DESC"]
    
    cursor = mydb.cursor()
    query = "AXIS_SP"
    cursor.callproc(query, (table,CD, PP,UD,CDesc,SD,FD,PD,"YEAR",SD))
    for result in cursor.stored_results():
        result = result.fetchall()
    # Do something with xaxis and yaxis here
    X=[]
    Y=[]
    for row in result:
        X.append(row[0])
        Y.append(row[1])

    with sns.axes_style('darkgrid'):
        plt.figure(figsize=(15, 5))
        plt.plot(X,Y,c="royalblue",linewidth = 2.5)
        # Plot Labels

        plt.xlabel("YEAR", fontsize=15, color='blue',fontweight='bold')
        plt.ylabel(SD,fontsize=15, color='blue',fontweight='bold')

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
        if os.path.exists('static/plot.png'):
            os.remove('static/plot.png')
        plt.savefig('static/plot.png')  # Save the plot image

        response = make_response(render_template('plot.html',random=random,data=final_d,column=columns))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = datetime.utcnow() - timedelta(days=1)
        response.headers['Pragma'] = 'no-cache'
        return response
    
if __name__ =='__main__':
    app.run(port=8080)
        
