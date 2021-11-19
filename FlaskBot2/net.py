from FlaskBot2.FlaskServer import FlaskServer

bot1 = FlaskServer()
bot1.run(port=7777)
print("!!!!!!!!!")
bot2 = FlaskServer()
bot2.run(port=7778)
