import streamlit as st
import numpy as np
from collections import Counter

_win_point = 5

BtnStyle = """
<style>
div.stButton > button:first-child {
    background-color: #6C4D94;
    color:#6C4D94;
    
}

div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
    
</style>"""

TicTacToe = """ <style> .font {font-size:50px ; font-family: 'Cooper Black'; color: #FF9633;} </style> """

st.markdown(BtnStyle, unsafe_allow_html=True)
st.markdown(TicTacToe, unsafe_allow_html=True)


X = '😀'
O = '🤖'
space = '🗯'


# From: https://stackoverflow.com/questions/39922967/python-determine-tic-tac-toe-winner
def checkRows(board):
#     st.write(board)
    for row in board:
        for i in range(0, len(row)):
            check_list = []
            for j in range(0,_win_point):
                if i <= (len(board)-_win_point):
                    check_list.append(row[i+j])

            count = Counter(check_list)
            if count[O] == _win_point:
                return O
            if count[X] == _win_point:
                return X

    return None




def checkDiagonals(board):
    # right Diagonals 
    for idx, row in enumerate(board):
        if idx <= (len(board)-_win_point):
            
            for i in range(len(row)):
                check_list = []
                for j in range(0,_win_point):
                    if i <= (len(board)-_win_point):
                        if j == 0:
                            check_list.append(row[i+j])
                        else:
                            check_list.append(board[idx+j][i+j])
                            
                count = Counter(check_list)

                if count[O] == _win_point:
                    return O
                if count[X] == _win_point:
                    return X

                
    # Left Diagonals           
    for idx, row in enumerate(board):
        if idx <= (len(board)-_win_point):
            
            for i in range(len(row)):
                check_list = []
                for j in range(0,_win_point):
                    if i >= (len(board)-_win_point-1):
                        if j == 0:
                            check_list.append(row[i+j])
                        else:
                            check_list.append(board[idx+j][i-j])
                            
#                 st.write(check_list)            
                count = Counter(check_list)

                if count[O] == _win_point:
                    return O
                if count[X] == _win_point:
                    return X

                
                
                
    return None


def checkWin(board):
    # transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
#         st.write('a')
    return checkDiagonals(board)


# Define callbacks to handle button clicks.
def handle_click(i, j):
    
    
    
    if not st.session_state.winner:
        # TODO: Handle the case when nobody wins but the game is over!
        st.session_state.board[i, j] = st.session_state.next_player
        
        if st.session_state.next_player == X:
            st.session_state.next_player = O
        else:
            st.session_state.next_player = X
            
        
        
        
def show():
    
    

    st.markdown('<p class="font">👾 Tic Tac Toe</p>', unsafe_allow_html=True)

    # Initialize state.
    if "board" not in st.session_state:
        st.session_state.board = np.full((8, 8), space, dtype=str)
        st.session_state.next_player = X
        st.session_state.winner = None
        
    st.header('Your Turn ' + st.session_state.next_player)

    
    # Show one button for each field.
    for i, row in enumerate(st.session_state.board):
        cols = st.beta_columns([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
                                ,0.07, 0.07])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )
    
    winner = checkWin(st.session_state.board)
    if winner != space:
        st.session_state.winner = winner
    
    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")


if __name__ == "__main__":
    show()




