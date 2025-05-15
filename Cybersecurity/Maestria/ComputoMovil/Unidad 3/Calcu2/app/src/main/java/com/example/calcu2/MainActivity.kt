package com.example.calcu2
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var txtResultado: EditText
    private var numero1: Double = 0.0
    private var operacionPendiente: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        txtResultado = findViewById(R.id.txtResultado)

        // Configurar listeners para todos los botones
        val botones = listOf(
            R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3, R.id.btn4,
            R.id.btn5, R.id.btn6, R.id.btn7, R.id.btn8, R.id.btn9,
            R.id.btnSumar, R.id.btnRestar, R.id.btnMultiplicar,
            R.id.btnDividir, R.id.btnIgual, R.id.btnLimpiar, R.id.btnPunto
        )

        botones.forEach { id ->
            findViewById<Button>(id).setOnClickListener { manejarBoton(id) }
        }
    }

    private fun manejarBoton(botonId: Int) {
        when (botonId) {
            R.id.btnLimpiar -> {
                txtResultado.text.clear()
                numero1 = 0.0
                operacionPendiente = ""
            }

            in listOf(R.id.btnSumar, R.id.btnRestar, R.id.btnMultiplicar, R.id.btnDividir) -> {
                numero1 = txtResultado.text.toString().toDoubleOrNull() ?: 0.0
                operacionPendiente = when (botonId) {
                    R.id.btnSumar -> "+"
                    R.id.btnRestar -> "-"
                    R.id.btnMultiplicar -> "×"
                    else -> "/"
                }
                txtResultado.text.clear()
            }

            R.id.btnIgual -> calcularResultado()
            else -> {
                val boton = findViewById<Button>(botonId)
                txtResultado.append(boton.text)
            }
        }
    }

    private fun calcularResultado() {
        val numero2 = txtResultado.text.toString().toDoubleOrNull() ?: 0.0
        val resultado = when (operacionPendiente) {
            "+" -> numero1 + numero2
            "-" -> numero1 - numero2
            "×" -> numero1 * numero2
            "/" -> if (numero2 != 0.0) numero1 / numero2 else Double.NaN
            else -> numero2
        }

        txtResultado.setText(
            if (resultado.isNaN()) "Error"
            else resultado.toString().removeSuffix(".0")
        )
        operacionPendiente = ""
    }
}