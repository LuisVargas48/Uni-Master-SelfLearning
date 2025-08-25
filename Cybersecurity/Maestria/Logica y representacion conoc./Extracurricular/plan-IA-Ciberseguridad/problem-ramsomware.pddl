(define (problem respuesta-ransomware-problem)
  (:domain respuesta-ransomware)

  (:objects
    m1 - maquina
    p21 p22 - puerto
  )

  ;; Estado inicial
  (:init
    (infectada m1)
    (puerto-abierto p21 m1)
    (puerto-abierto p22 m1)
    (respaldo-disponible m1)
  )

  ;; Objetivo: máquina segura y CSIRT notificado
  (:goal
    (and
      (segura m1)
      (notificado-csirt)
      (puerto-cerrado p21 m1)
      (puerto-cerrado p22 m1)
    )
  )
)
