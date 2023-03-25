import berserk
import datetime as DT
import globals
import io
import chess
import chess.engine
from stockfish import Stockfish
import chess.pgn
import cairosvg

def grab_games():
	# Authentication
	token = '' # Todo: update LiChess token from .env file
	session = berserk.TokenSession(token)
	globals.lichess_client = berserk.Client(session)
	globals.lichess_account = globals.lichess_client.account.get()
	globals.rating_history = globals.lichess_client.users.get_rating_history(globals.username)
	globals.public_data = globals.lichess_client.users.get_public_data(globals.username)
	globals.gms = globals.lichess_client.games.export_by_player(
            globals.username, since=int(berserk.utils.to_millis(DT.datetime.strptime(globals.startdate, "%Y-%m-%d"))),
            until=int(berserk.utils.to_millis(DT.datetime.strptime(globals.enddate, "%Y-%m-%d"))),
            max=500,
            as_pgn=True)
	globals.games = list(globals.gms)
	globals.num_games = len(globals.games)
	globals.cur_game = 0
	globals.cur_move = 0
	#print(globals.games[globals.cur_game])


def load_board():
	pgn = io.StringIO(globals.games[globals.cur_game])
	globals.chess_game = chess.pgn.read_game(pgn)
	board = globals.chess_game.board()
	globals.svg_results = []
	globals.svg_results.append(chess.svg.board(board=board))
	move_iter = 0
	open(f"images/out{move_iter}.svg", 'w').write(globals.svg_results[move_iter])	
	for move in globals.chess_game.mainline_moves():
		board.push(move)
		globals.svg_results.append(chess.svg.board(board=board))
		move_iter+=1
		open(f"images/out{move_iter}.svg", 'w').write(globals.svg_results[move_iter])	
	globals.total_moves = move_iter	
	globals.cur_move = 0
	

def update_board_img():		
	cairosvg.svg2png(url=f"images/out{globals.cur_move}.svg", write_to="images/output.png")
	
def analyze_board():
	engine = chess.engine.SimpleEngine.popen_uci("stockfish")
	board = globals.chess_game.board()
	for move in globals.chess_game.mainline_moves():
		info = engine.analyse(board, chess.engine.Limit(time=0.1))			
		print("Score:", info["score"])
		board.push(move)
	
