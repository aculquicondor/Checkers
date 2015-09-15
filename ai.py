from operator import __lt__, __gt__

from game import Table


def play(table, levels=7):
    _, move = _play(table, levels, table.turn)
    return move


def _play(table, levels, player, alpha=-64, beta=64):
    move = None
    if not levels:
        return table.points(player), move

    result, comparator = (-64, __gt__) if table.turn == player else \
        (64, __lt__)

    for row, col in table.positions():
        if alpha >= beta:
            break

        for r, c, e in table.moves(row, col):
            if alpha >= beta:
                break

            new_table = Table(table)
            new_table.unchecked_move((row, col), (r, c), e)
            t_result, _ = _play(new_table, levels - 1, player, alpha, beta)

            if comparator(t_result, result):
                result = t_result
                move = (row, col), (r, c), e
                if table.turn == player:
                    alpha = result
                else:
                    beta = result

    return result, move
