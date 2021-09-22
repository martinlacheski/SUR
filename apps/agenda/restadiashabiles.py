from datetime import date, timedelta, datetime

fechaNotificaion = date(2021, 9, 27)
diasHabRestados = 0
resultado = date.today()
diasAntelacion = 4
fechaResultado = fechaNotificaion

# funciona
while diasHabRestados < diasAntelacion:
    fechaResultado =  fechaResultado - timedelta(days=1)
    print("Fecha resultado ", fechaResultado)
    if fechaResultado.weekday() in range(5):
        print("restamos día hábil", diasHabRestados)
        diasHabRestados = diasHabRestados + 1


print(fechaResultado)
