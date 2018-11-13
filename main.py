'''
main.py
'''
import logging, os
from datetime import datetime
import game, config
import numpy as np #DEBUG

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    logfilename = os.path.join(
            'logs', 
            datetime.now().strftime('%Y-%m-%d--%H-%M-%S')+'.log')
    logging.basicConfig( 
        level=logging.DEBUG, 
        handlers=[
            logging.FileHandler(logfilename),
            logging.StreamHandler()
        ])

    g = game.Game(config.SERVER_URL, config.UID)
    state = g.get_state()
    logging.info('Server connection initiated. Game starting...')
    logging.info('New maze: ' + str(state))

    while(state['status'] == game.STATUS['PLAYING']):
        stack   = []
        visited = set()
        current = state['current_location']

        #DEBUG
        mapper = []
        for i in range(0, state['maze_size'][1]):
            row = []
            for i in range(0, state['maze_size'][0]):
                row.append(0)
            mapper.append(row)

        while current is not None:
            stack.append(current)
            visited.add(tuple(current))
            mapper[current[1]][current[0]] = 7 #DEBUG
            didMove = False

            print(np.matrix(mapper))
            logging.debug('Current location: {}, Stack: {}'.format(str(g.get_state()['current_location']), str(stack)))
            for action in game.ACTION:
                nextCoord = _next_coordinate(current, action)
                if(_in_maze(state['maze_size'], nextCoord) and tuple(nextCoord) not in visited):
                    res = g.do_action(action)
                    if(res['result'] == game.RESULT['WALL']):
                        visited.add(tuple(nextCoord))
                        logging.debug('Wall hit at location: ' + str(nextCoord))
                        mapper[nextCoord[1]][nextCoord[0]] = 8 #DEBUG
                    elif(res['result'] == game.RESULT['SUCCESS']):
                        mapper[current[1]][current[0]] = 1 #DEBUG
                        current = nextCoord
                        logging.debug('Moved to location: ' + str(nextCoord))
                        didMove = True
                        break
                    elif(res['result'] == game.RESULT['OUT_OF_BOUNDS']):
                        logging.critical('Error: Moved out of bounds, location: ' + str(nextCoord))
                        return
                    elif(res['result'] == game.RESULT['END']):
                        logging.debug('Moved to location: ' + str(nextCoord))
                        logging.info('Maze ' + str(state['levels_completed']+1) + ' completed!')
                        current = None
                        didMove = True
                        break

            if not didMove:
                # Backtrack
                current = stack.pop()
                prev    = stack.pop()
                mapper[current[1]][current[0]] = 1 #DEBUG
                g.do_action(_get_direction(current, prev))
                current = prev
                mapper[current[1]][current[0]] = 7 #DEBUG
                logging.debug('Backtracked to location: ' + str(prev))

        state = g.get_state()
        logging.info('New maze: ' + str(state))

    state = g.get_state()
    if(state['status'] == game.STATUS['PLAYING']):
        logging.critcal('Error: Ending reached but game is not finished!')
    elif(state['status'] == game.STATUS['GAME_OVER']):
        logging.critical('Error: Game over!')
    elif(state['status'] == game.STATUS['NONE']):
        logging.critical('Error: Session expired!')
    elif(state['status'] == game.STATUS['FINISHED']):
        logging.info('Game finished!')



def _next_coordinate(current, action):
    copy = current.copy()
    if(action == game.ACTION['UP']):
        copy[1] = copy[1]-1      
    elif(action == game.ACTION['DOWN']):
        copy[1] = copy[1]+1
    elif(action == game.ACTION['LEFT']):
        copy[0] = copy[0]-1        
    elif(action == game.ACTION['RIGHT']):
        copy[0] = copy[0]+1
    return copy

def _in_maze(maze_size, loc):
    return loc[0] >= 0 and loc[1] >= 0 and loc[0] < maze_size[0] and loc[1] < maze_size[1]

def _get_direction(loc1, loc2):
    if(loc1[0] < loc2[0]):
        return game.ACTION['RIGHT']
    elif(loc1[0] > loc2[0]):
        return game.ACTION['LEFT']
    elif(loc1[1] > loc2[1]):
        return game.ACTION['UP']
    elif(loc1[1] < loc2[1]):
        return game.ACTION['DOWN']

if __name__ == '__main__':
    main()