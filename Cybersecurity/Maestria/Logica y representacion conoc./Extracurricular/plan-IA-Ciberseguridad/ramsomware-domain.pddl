(define (domain respuesta-ransomware)
  (:requirements :strips :typing :negative-preconditions)
  (:types maquina puerto)
  
  (:predicates
    (infectada ?m - maquina)
    (aislada ?m - maquina)
    (puerto-abierto ?p - puerto ?m - maquina)
    (puerto-cerrado ?p - puerto ?m - maquina)
    (respaldo-disponible ?m - maquina)
    (restaurada ?m - maquina)
    (notificado-csirt)
    (segura ?m - maquina)
  )

  ;; Acción 1: Aislar máquina infectada
  (:action aislar-maquina
    :parameters (?m - maquina)
    :precondition (infectada ?m)
    :effect (aislada ?m)
  )

  ;; Acción 2: Cerrar puertos
  (:action cerrar-puerto
    :parameters (?m - maquina ?p - puerto)
    :precondition (puerto-abierto ?p ?m)
    :effect (and (puerto-cerrado ?p ?m) (not (puerto-abierto ?p ?m)))
  )

  ;; Acción 3: Notificar al CSIRT
  (:action notificar-csirt
    :parameters ()
    :precondition (and)
    :effect (notificado-csirt)
  )

  ;; Acción 4: Restaurar desde respaldo
  (:action restaurar-maquina
    :parameters (?m - maquina)
    :precondition (and (aislada ?m) (respaldo-disponible ?m))
    :effect (and (restaurada ?m) (segura ?m) (not (infectada ?m)))
  )
)

