.SYSDATA
SWITCH MESSAGES        ON 
SWITCH AUTOSTART.PC    ON
SWITCH AUTOSTART2.PC   ON
.END
.PROGRAM autostart.pc()
	CALL serial
.END
.PROGRAM autostart2.pc()
	CALL control
.END
.PROGRAM control()
	DO
		CASE start_cycle OF
            VALUE -1
;robot work
				last_timer = TIMER(9)
				time_work = time_work + last_timer
				start_cycle = 0
				TIMER (9) = 0
				SIGNAL -o_Alarm
			VALUE 0
;start stop robot
				IF TIMER(9) >= 20 THEN					
					last_timer = TIMER(9)
					time_rest = time_rest + last_timer
					start_cycle = 1
					TIMER (9) = 0
				END
;stop mavhine
			VALUE 1
				IF TIMER(9) >= 1 THEN					
					last_timer = TIMER(9)
					time_rest = time_rest + last_timer
					TIMER (9) = 0
					SIGNAL o_Alarm
				END
		END
	UNTIL flg_run == 0
.END
.PROGRAM wysciolka()
1       IF SIG(praca) THEN
			TWAIT czas2
			IF SIG(pos1) AND SIG(praca) THEN
				IF SIG (i_rasp) == FALSE THEN
					ACCURACY 100 ALWAYS
					JMOVE pos1
					TWAIT startw
					ACCURACY 1
					SWAIT (-pauza)
					start_cycle = -1
					count_pod = count_pod + 1
					SIGNAL prasa
					TWAIT 0.1
					JMOVE pos2
					SIGNAL (zlap)
					TWAIT czekaj
					SPEED 50
					SWAIT (-pauza)
					ACCURACY 150 ALWAYS
					JMOVE pos1
					SPEED 100
					SWAIT (-pauza)
					ACCURACY 200
					C1MOVE park
					SWAIT (-pauza)
					ACCURACY 10
					C2MOVE pok1
					SPEED 400 MM/S ALWAYS
					SWAIT (-pauza)
					SWAIT (ssil)
					TWAIT 0.1
					ACCURACY 10
					LMOVE pok2
					SWAIT (-pauza)
					SPEED 100 ALWAYS
					IF SIG(drugi) THEN
						C1MOVE pok3
						SWAIT (-pauza)
						C2MOVE pok4
						SPEED 350 MM/S ALWAYS
						SWAIT (-pauza)
						ACCURACY 10
						LMOVE pok5
					ELSE
						SWAIT (-pauza)
					END
					SPEED 100 ALWAYS	
					ACCURACY 100
					IF SIG(wybor) THEN
						SWAIT (-pauza)
						JMOVE kontrola
						SWAIT (-pauza)
						TWAIT klej
					ELSE
						SWAIT (-pauza)
					END
					ACCURACY 100 ALWAYS
					C1MOVE pos3_1
					C2MOVE pos3
					SWAIT (-pauza)
					ACCURACY 1
					SPEED 500 MM/S ALWAYS
					SWAIT (-pauza)
					JMOVE pos4
					TWAIT sklej
					SIGNAL (-prasa)
					SIGNAL (-zlap)				
					SIGNAL (pusc)
					TWAIT tzrzut
					SIGNAL (-pusc)
					SWAIT (-pauza)
					ACCURACY 100 ALWAYS
					SPEED 100 ALWAYS
					C1MOVE pos3
					PULSE (auto),1
					C2MOVE pos1
					TWAIT obrot
					GOTO 1
				ELSE

; pause empty table
; back to pos under table
					JMOVE pos1
					SIGNAL prasa
					ty "pass"
					TWAIT 4
					SIGNAL (-prasa)
; check pauza
					SWAIT (-pauza)
					TWAIT sklej
					PULSE (auto),1
					TWAIT obrot
					GOTO 1					
				END
			END
		ELSE
			IF SIG(-praca) THEN
				SWAIT (-pauza)
				JMOVE park
				TWAIT 2
				JMOVE park2
				SWAIT (praca)
			END
		END
.END
.PROGRAM serial()
;*********Parameters of connection***********
  SETSIO 19200,1
  PROTOCOL 1,1,1,3,3,0
  PROTRESET
;*****************************************
  $st_in = ""
  $st_out = ""
  $temp = ""
  $command = ""
  $data = ""
	DO
		.r_err = 0
		.s_err = 0
		RECEIVE $st_in,.r_err
		IF .r_err==0 THEN
			$temp = $DECODE($st_in,",",0)
			$command = $temp
			$temp = $DECODE($st_in,",",1)
			$data = $st_in
			IF $command=="ONLINE" THEN			
				$st_out = $ENCODE(/F8.2,last_timer) + "," + $ENCODE(/F8.2,count_pod) + "," + $ENCODE(/F8.2,time_work) + "," + $ENCODE(/F8.2,time_rest)
				SEND "ONLINE_OK," + $st_out, .s_err
			END
			IF $command=="ZERO_COUNTER" THEN
				count_pod = 0
				time_work = 0
				time_rest = 0
				SEND "ZERO_COUNTER_OK,1", .s_err
			END
			IF $command=="GET_MACHINE_NAME" THEN			
				$st_out = "GET_NAME,"+$machine_name
				SEND $st_out, .s_err
			END	
			IF $command=="GET_MACHINE_ARTICLE" THEN							
				$st_out = "GET_ARTICLE,"+$machine_article
				SEND $st_out, .s_err
			END
			IF $command=="GET_MACHINE_CZEKAJ" THEN							
				$st_out = "GET_CZEKAJ," + $ENCODE(/F8.2,czekaj)
				SEND $st_out, .s_err
			END				
			IF $command=="GET_POK1" THEN							
				DECOMPOSE .a[0] = pok1
				$st_out = "GET_POK1,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_POK2" THEN							
				DECOMPOSE .a[0] = pok2
				$st_out = "GET_POK2,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_POS1" THEN							
				DECOMPOSE .a[0] = pos1
				$st_out = "GET_POS1,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_POS2" THEN							
				DECOMPOSE .a[0] = pos2
				$st_out = "GET_POS2,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_POS3" THEN							
				DECOMPOSE .a[0] = pos3
				$st_out = "GET_POS3,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_POS4" THEN							
				DECOMPOSE .a[0] = pos4
				$st_out = "GET_POS4,"
				FOR .I = 0 TO 5
					$st_out = $st_out + $ENCODE(/F8.2,.a[.I]) + ","
				END
				SEND $st_out, .s_err					
			END
			IF $command=="GET_MACHINE_FINISH" THEN							
				$st_out = "GET_FINISH,1"
				SEND $st_out, .s_err
			END
			IF $command=="PUT_MACHINE_NAME" THEN
				$temp = $DECODE($st_in,",",0)
				$command = $temp			
				$machine_name=$command
				SEND "PUT_NAME,0", .s_err		ІІІІ
			END
			IF $command=="PUT_MACHINE_ARTICLE" THEN
				$temp = $DECODE($st_in,",",0)
				$command = $temp
				$machine_article=$command
				SEND "PUT_ARTICLE,0", .s_err							
			END
			IF $command=="PUT_MACHINE_CZEKAJ" THEN
				$temp = $DECODE($st_in,",",0)
				$command = $temp
				czekaj=VAL($command)
				SEND "PUT_CZEKAJ,0", .s_err							
			END	
			IF $command=="PUT_POK1" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)						
					$temp = $DECODE($data,",",1)	
				END					
				POINT pok1 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POK1,0", .s_err							
			END				
			IF $command=="PUT_POK2" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)						
					$temp = $DECODE($data,",",1)	
				END					
				POINT pok2 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POK2,0", .s_err							
			END				
			IF $command=="PUT_POS1" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)				І		
					$temp = $DECODE($data,",",1)	
				END					
				POINT pos1 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POS1,0", .s_err							
			END				
			IF $command=="PUT_POS2" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)						
					$temp = $DECODE($data,",",1)	
				END					
				POINT pos2 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POS2,0", .s_err							
			END				
			IF $command=="PUT_POS3" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)						
					$temp = $DECODE($data,",",1)	
				END					
				POINT pos3 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POS3,0", .s_err							
			END				
			IF $command=="PUT_POS4" THEN					
				FOR .i=0 TO 5
					$temp = $DECODE($data,",",0)
					.t_p[.i] = VAL($temp)						
					$temp = $DECODE($data,",",1)	
				END					
				POINT pos4 = TRANS(.t_p[0],.t_p[1],.t_p[2],.t_p[3],.t_p[4],.t_p[5])				
				SEND "PUT_POS4,0", .s_err							
			END								
			IF $command=="PUT_MACHINE_FINISH" THEN
				SEND "PUT_FINISH,0", .s_err		
			END
			IF .s_err==0 THEN
				;TYPE "SEND OK"
			END			
		END
	UNTIL flg_run == 0
.END
.REALS
o_Alarm = 15
last_timer = -1
time_work = 0
time_rest = 0
start_cycle = 0
flg_run = -1
count_pod = 0
pos1  = 1001
praca = 1002
pauza = 1003
drugi = 1005
wybor = 1006
ssil  = 1007
i_rasp = 1008
prasa  = 1 ; it is sole_press out sig
zlap   = 2
pusc   = 3
auto = 5
.END
