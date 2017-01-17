#!/usr/bin/python
#_*_ coding: utf-8 _*_

# Importar as bibliotecas utilizadas
import RPi.GPIO as G
from flup.server.fcgi import WSGIServer
import sys, urlparse
import math

# Setup da Biblioteca RPIO
G.setwarnings(False) 
G.setmode(G.BCM)

# Setup Motor AB (Direito)
G.setup(19, G.OUT) # Amarelo (Pino A - Terminal do Motor próximo ao chassis)
G.setup(26, G.OUT) # Laranja (Pino B - Terminal do Motor próximo ao chão) 
G.setup(21, G.OUT) # PWM Motor AB
pwmR = G.PWM(21,200)
pwmR.start(0)

# Setup Motor CD (Esquerdo)
G.setup(6,G.OUT)   # Vermelho (Pino C - Terminal do Motor próximo ao chassis)
G.setup(13,G.OUT)  # Marrom   (Pino D - Terminal do Motorpróximo ao chão)
G.setup(20,G.OUT)  # PWM Motor CD
pwmL = G.PWM(20, 200)
pwmL.start(0)

# Setup da MAX VELOCIDADE
max_speed = 100
min_speed = 5
vel = 0

# Main loop
def app(environ, start_response):
	
	# Recebe e interpreta mensagem enviada via HTML / Javascript na home page
	start_response("200 OK", [("Content-Type","text/html")])
	params = urlparse.parse_qs(environ["QUERY_STRING"])
	yield('&nbsp;')
	
	if "x" in params:
		str_dx = params["x"][0]
		dx = int(str_dx)	# Converte string recebida em inteiro
	if "y" in params:
		str_dy = params["y"][0]
		dy = int(str_dy)	# Converte string recebida em inteiro
	
	vel = math.hypot(dx,dy) # calculo do módulo da velocidade	

	# Analisa os valores de 0-100 recebidos para os eixos X e Y
	# e calcula as direções e velocidades de cada motor
	if dy == 0:
		pwmR.ChangeDutyCycle(0)
                pwmL.ChangeDutyCycle(0)

	if dy < -5: # Verifica se o joystick está indo para FRENTE
		# Polariza os motores para andar para frente
		G.output(26 , True )
		G.output(19 , False)
		G.output(6  , True )
		G.output(13 , False)
		if dx > -10 and dx < 10:
			# 10 unidades de margem sem fazer curvas
			pwmL.ChangeDutyCycle(vel)
			pwmR.ChangeDutyCycle(vel)
		if dx >= 10:   # Curva para direita
			pwmL.ChangeDutyCycle(vel - dx)
			pwmR.ChangeDutyCycle(vel)
		if dx <= -10:   # Curva para esquerda
			pwmL.ChangeDutyCycle(vel)
                	pwmR.ChangeDutyCycle(vel + dx)
		if dx == 0 and dy == 0:
			pwmL.ChangeDutyCycle(0)
			pwmR.ChangeDutyCycle(0)

	if dy > 5: # Verifica se o joystick está indo para TRAS
		# Polariza os motores para andar para tras
		G.output(26 , False)
                G.output(19 , True)
                G.output(6  , False)
                G.output(13 , True)
		if dx > -10 and dx < 10:
                        # 10 unidades de margem sem fazer curvas
			pwmL.ChangeDutyCycle(vel)
                        pwmR.ChangeDutyCycle(vel)
                if dx >= 10:  # Curva para esquerda
                        pwmL.ChangeDutyCycle(vel - dx)
                        pwmR.ChangeDutyCycle(vel)
                if dx <= -10:   # Curva para direita
                        pwmL.ChangeDutyCycle(vel)
                        pwmR.ChangeDutyCycle(vel + dx)
                if dx == 0 and dy == 0:
                        pwmL.ChangeDutyCycle(0)
                        pwmR.ChangeDutyCycle(0)
	
#Executa este app que monitora as chamadas de Fast CGI da página HTML
WSGIServer(app).run()
