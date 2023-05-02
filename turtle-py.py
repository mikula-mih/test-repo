import turtle as tr

tr.speed(0)
tr.bgcolor("black")
tr.pencolor("orange")

for s in range(155):
    tr.rt(s)
    tr.circle(125, s)
    tr.fd(s)
    tr.rt(90)

tr.done()
