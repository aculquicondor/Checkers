from operator import __lt__, __gt__


def play(table, levels=8):
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

            mv_args = (row, col), (r, c), e
            table.unchecked_move(*mv_args)
            t_result, _ = _play(table, levels - 1, player, alpha, beta)
            table.restore_move(*mv_args)

            if comparator(t_result, result):
                result = t_result
                move = (row, col), (r, c), e
                if table.turn == player:
                    alpha = result
                else:
                    beta = result

    return result, move
