import numberletters

str_numero = numberletters.a_numero("777")
if str_numero == "setecientos setenta y siete":
    print("OK")
else:
    print("BAD")

str_numero = numberletters.a_numero("7")
if str_numero == "siete":
    print("OK")
else:
    print("BAD")

str_numero = numberletters.a_numero("100")
if str_numero == "cien":
    print("OK")
else:
    print("BAD")