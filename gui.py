import tkinter as tk
import tkinter.simpledialog
import datetime as dt
from lichess import *
import webbrowser
import cairosvg
import chess
import chess.pgn
import chess.engine
import globals
from io import StringIO

def chess_copilot_gui():

    # Create the main window
    window = tk.Tk()
    window.title("Chess CoPilot")


    def update_board_data():
        globals.cur_game_pgn = chess.pgn.read_game(StringIO(globals.games[globals.cur_game]))
        gamenum_label["text"] = f"{globals.cur_game+1}"
        gamedate_label["text"] = globals.cur_game_pgn.headers["Date"]
        gameevent_label["text"] = globals.cur_game_pgn.headers["Event"]
        #gameurl_label["text"] = globals.cur_game.pgn.headers["Site"]
        gamewhite_label["text"] = globals.cur_game_pgn.headers["White"]
        gameblack_label["text"] = globals.cur_game_pgn.headers["Black"]
        gameresult_label["text"] = globals.cur_game_pgn.headers["Result"]
        
        
    def onPrevGame():
        globals.cur_game = globals.cur_game - 1
        if (globals.cur_game < 0):
            globals.cur_game = 0
        load_board()
        update_board_img()
        update_board_data()
        displayBoardImg()



	
    def onNextGame():
        globals.cur_game = globals.cur_game + 1
        if (globals.cur_game > globals.num_games):
            globals.cur_game = globals.num_games
        load_board()
        update_board_img()
        update_board_data()
        displayBoardImg()
        #analyze_board()
					
	
    def onNextMove():
        globals.cur_move = globals.cur_move + 1
        if (globals.cur_move > globals.total_moves):
            globals.cur_move = globals.total_moves
        displayBoardImg()
        
    def onPrevMove():
        globals.cur_move = globals.cur_move - 1
        if (globals.cur_move < 0):
            globals.cur_move = 0
        displayBoardImg()
        
        
    def onFirstMove():
        globals.cur_move = 0
        displayBoardImg()
        
    def onLastMove():
        globals.cur_move = globals.total_moves
        displayBoardImg()
	

    def displayBoardImg():
        update_board_img()
        globals.board_img = tk.PhotoImage(file='images/output.png')
        chess_board_label["image"]=globals.board_img
	
			

    def onload():
        loadbutton["state"] = tk.DISABLED
			
        return_label["text"] = "Loading...please wait"
        globals.startdate = startdate_entry.get()
        globals.enddate = enddate_entry.get()
        globals.username = username_entry.get()
        grab_games()
			
        return_label["text"] = f"Returned {globals.num_games} games"
        loadbutton["state"] = tk.NORMAL
        chess_next_button["state"] = tk.NORMAL
        chess_prev_button["state"] = tk.NORMAL
        chess_first_button["state"] = tk.NORMAL
        chess_last_button["state"] = tk.NORMAL
        game_next_button["state"] = tk.NORMAL
        game_prev_button["state"] = tk.NORMAL
			
			
        username_label["text"] = globals.username
        url = globals.public_data["url"]
        username_url["text"] = url
        if (globals.public_data["online"] == 0):
            online_label["text"] = "Status: Offline"
            online_label.config(fg="Red")
        else:
            online_label["text"] = "Status: Online"
            online_label.config(fg="Green")
					
        rating_label["text"] = globals.public_data["perfs"]["rapid"]["rating"]
        load_board()
        update_board_img()
        update_board_data()
        displayBoardImg()
        #analyze_board()

				
    def username_urlcallback():
        url = globals.public_data["url"]
        print(globals.startdate)
        webbrowser.open_new(url)	

		
	
	
    window.configure(bg="dark slate blue")

    # Top frame, includes the user/date select and user info frames
    top_frame = tk.Frame(window,
                         bg="dark slate blue",
                         highlightcolor="white smoke",
                         highlightthickness=1,
                         width=1200,
                         height=300,
                         bd=2)
    top_frame.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.N)

    # Middle frame, includes the game display and board display frames
    middle_frame = tk.Frame(window,
                            highlightcolor="white smoke",
                            highlightthickness=1,
                            width=1200,
                            height=600,
                            bd=2)
    middle_frame.pack(side=tk.TOP, fill=tk.Y, expand=1, anchor=tk.N)

	# Chess game data frame
    chess_game_data_frame = tk.Frame(middle_frame,
                                width=600,
                                height=600,
                                bg="dark slate blue",
                                highlightbackground="white smoke",
                                highlightcolor="white smoke",
                                highlightthickness=1)
    chess_game_data_frame.pack(side=tk.LEFT, fill=tk.Y, expand=1, anchor=tk.W)   
    chess_game_data_labels = tk.Frame(chess_game_data_frame,
                            width=600,
                                height=600,
																			padx=5,
                                 pady=5,
                                 bg="dark slate blue")
    chess_game_data_labels.grid(row=0, column=0)
    tk.Label(chess_game_data_labels,
             text='Game #: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=0, column=0)
    tk.Label(chess_game_data_labels,
             text='Date: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=1, column=0)
    tk.Label(chess_game_data_labels,
             text='Event: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=2, column=0)
    tk.Label(chess_game_data_labels,
             text='Site: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=3, column=0)

    tk.Label(chess_game_data_labels,
             text='White: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=4, column=0)
    tk.Label(chess_game_data_labels,
             text='Black: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=5, column=0)
    tk.Label(chess_game_data_labels,
             text='Result: ',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").grid(row=6, column=0)
    gamenum_label = tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gamenum_label.grid(row=0, column=1)
    gamedate_label = tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gamedate_label.grid(row=1, column=1)
    gameevent_label=tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gameevent_label.grid(row=2, column=1)
    gameurl_label=tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gameurl_label.grid(row=3, column=1)

    gamewhite_label=tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gamewhite_label.grid(row=4, column=1)
    gameblack_label=tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gameblack_label.grid(row=5, column=1)
    gameresult_label= tk.Label(chess_game_data_labels,
             text='',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke")
    gameresult_label.grid(row=6, column=1)
    
    
    game_prev_button = tk.Button(chess_game_data_labels,
                           text='Prev Game',
                           command=onPrevGame,
                           padx=5,
                           pady=5, state=tk.DISABLED)
    game_prev_button.grid(row=7, column = 0)


    game_next_button = tk.Button(chess_game_data_labels,
                           text='Next Game',
                           command=onNextGame,
                           padx=5,
                           pady=5, state=tk.DISABLED)
    game_next_button.grid(row=7, column = 1)
	

	
	# Chess game board frame
    chess_game_board_frame = tk.Frame(middle_frame,
                                width=600,
                                height=600,
                                bg="dark slate blue",
                                highlightbackground="white smoke",
                                highlightcolor="white smoke",
                                highlightthickness=1)
    chess_game_board_frame.pack(side=tk.RIGHT, fill=tk.X, expand=1, anchor=tk.E)  
    
    globals.board_img = tk.PhotoImage(file='images/default.png')
    chess_board_label = tk.Label(chess_game_board_frame, bg="dark slate blue", image=globals.board_img)
    chess_board_label.grid(row=1, rowspan=4, column=3)
    chess_next_button = tk.Button(chess_game_board_frame,
                           text='▶',
                           command=onNextMove,
                           padx=5,
                           pady=5, state=tk.DISABLED)

    chess_next_button.grid(row=1, column=1)
    chess_prev_button = tk.Button(chess_game_board_frame,
                           text='◀',
                           command=onPrevMove,
                           padx=5,
                           pady=5, state=tk.DISABLED)
    chess_prev_button.grid(row=2, column=1)
    chess_first_button = tk.Button(chess_game_board_frame,
                           text='F',
                           command=onFirstMove,
                           padx=5,
                           pady=5, state=tk.DISABLED)

    chess_first_button.grid(row=3, column=1)
    chess_last_button = tk.Button(chess_game_board_frame,
                           text='L',
                           command=onLastMove,
                           padx=5,
                           pady=5, state=tk.DISABLED)

    chess_last_button.grid(row=4, column=1)


	
    # Bottom frame, includes the game analysis frame
    bottom_frame = tk.Frame(window,
                            highlightcolor="white smoke",
                            highlightthickness=1,
                            width=1200,
                            height=300,
                            bd=2)
    bottom_frame.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.N)

    # User input frame
    user_input_frame = tk.Frame(top_frame,
                                width=600,
                                height=600,
                                bg="dark slate blue",
                                highlightbackground="white smoke",
                                highlightcolor="white smoke",
                                highlightthickness=1)
    user_input_frame.pack(side=tk.LEFT, fill=tk.X, expand=1, anchor=tk.W)

    user_input_labels = tk.Frame(user_input_frame,
                                 padx=5,
                                 pady=5,
                                 bg="dark slate blue")
    user_input_labels.grid(row=0, column=1)
    tk.Label(user_input_labels,
             text='Lichess User:',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").pack(anchor=tk.E)
    tk.Label(user_input_labels,
             text='Start Date:',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").pack(anchor=tk.E)
    tk.Label(user_input_labels,
             text='End Date:',
             padx=5,
             pady=5,
             bg="dark slate blue",
             bd="0",
             fg="white smoke").pack(anchor=tk.E)

    user_input_inputs = tk.Frame(user_input_frame,
                                 padx=5,
                                 pady=5,
                                 bg="dark slate blue")
    user_input_inputs.grid(row=0, column=2)

    username_entry = tk.Entry(user_input_inputs,
                              bg="white smoke",
                              bd="0",
                              fg="black")
    username_entry.insert(0, "jzambreno")
    username_entry.pack(padx=5, pady=5)

    td0 = dt.date.today()
    td = td0 + dt.timedelta(days=-1)
    tdback = td - dt.timedelta(days=365)

    startdate_entry = tk.Entry(user_input_inputs,
                               bg="white smoke",
                               bd="0",
                               fg="black")
    startdate_entry.insert(0, tdback)
    startdate_entry.pack(padx=5, pady=5)
    enddate_entry = tk.Entry(user_input_inputs,
                             bg="white smoke",
                             bd="0",
                             fg="black")
    enddate_entry.insert(0, td)
    enddate_entry.pack(padx=5, pady=5)
    loadbutton = tk.Button(user_input_frame,
                           text='Load',
                           command=onload,
                           padx=5,
                           pady=5)
    loadbutton.grid(row=1, column=1)

    return_label = tk.Label(user_input_frame,
                            text='',
                            padx=5,
                            pady=5,
                            bg="dark slate blue",
                            bd="0",
                            fg="white smoke")
    return_label.grid(row=1, column=2)

    # User info frame
    user_info_frame = tk.Frame(top_frame,
                               width=600,
                               height=600,
                               bg="dark slate blue",
                               highlightbackground="white smoke",
                               highlightcolor="white smoke",
                               highlightthickness=1)
    user_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=1, anchor=tk.E)
    username_label = tk.Label(user_info_frame,
                              text='',
                              padx=5,
                              pady=5,
                              bg="dark slate blue",
                              bd="0",
                              fg="white smoke")
    username_label.grid(row=1, column=1)

    online_label = tk.Label(user_info_frame,
														text = '',
														padx = 5,
														pady = 5,
														bg = "dark slate blue",
														bd = 0,
														fg = "white smoke")
                                                        
    online_label.grid(row = 2, column = 1)

    rating_label = tk.Label(user_info_frame,
													 text = '',
													 padx = 5,
													 pady = 5,
													 bg = "dark slate blue", 
													 bd = 0,
													 fg = "white smoke")
    rating_label.grid(row = 2, column = 3)
	
    username_url = tk.Label(user_info_frame, cursor="hand2",text='',padx=5,pady=5,bg="dark slate blue", bd="0",fg="blue")
    username_url.grid(row=1, column=2)
    username_url.bind("<Button-1>", lambda e: username_urlcallback())	

    
    
    tk.mainloop()
