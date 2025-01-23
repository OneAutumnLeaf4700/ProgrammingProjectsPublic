//Import required dependencies
const lobbyManager = require('./lobbyManager');
const { Chess } = require('./chess.js-0.13.4/chess.js-0.13.4/chess.js');


// ---------------------------------
// Game Lobbies
// --------------------------------

module.exports = (io) => {
    
    
    // ---------------------------------
    // Server functions
    // --------------------------------
    
    function createMultiplayerGame(userId) {
        const gameId = lobbyManager.createMultiplayerGame(userId);
        return gameId;
    };

    // New function to handle player assignment and send turn assignment notification to user
    async function assignPlayerColor(socket, userId, gameId) {
        const color = await lobbyManager.getPlayerColor(userId, gameId);
        console.log(`Assigning color ${color} to player ${userId}`);
        socket.emit('colorAssignment', color);
    }
    
    // New function to handle player assignment and turn notification
    async function getCurrentTurn(socket, gameId) {
        const turn = await lobbyManager.getCurrentTurn(gameId);
        socket.emit('currentTurn', turn);
    }

    // Sync Boards
    function syncBoard(socket, gameState) {
        socket.emit('syncBoard', gameState);
    }

    // Update the board
    async function handleReconnect(socket, gameId) {
        const game = await lobbyManager.getGame(gameId);
        socket.emit('updateBoard', game.gameState.fen);
    }

    // Make the move on the remaining client sides
    function makeMoveOnClientSide(socket, move) {
        socket.broadcast.emit('opponentMove', move)
    };
    
    // Making a move
    async function handleMove(io, socket, gameId, gameState) {
        //Save new data
        const game = await lobbyManager.updateGameState(gameId, gameState);
        console.log('Game state updated:', game);

        // Make the move on the remaining client sides
        makeMoveOnClientSide(socket, gameState.move);

        //Update the turn on the client side
        getCurrentTurn(io, gameId);

    }

    // ---------------------------------
    // Socket.io events
    // --------------------------------

    // Listen for connections
    io.on('connection', socket => {
        
        
        // ---------------------------------
        // Multiplayer events
        // --------------------------------
        
        
        socket.on('userConnected', (userId, gameId) => {
            // Handle user reconnection (sync board, handle player assignment, etc.)
            handleReconnect(socket, gameId);
            assignPlayerColor(socket, userId, gameId);
            getCurrentTurn(socket, gameId);
        });

        // Creating a new multiplayer game
        socket.on('newMultiplayerGameRequested', async (userId) => {
            try {
                const gameId = await createMultiplayerGame(userId); // Get the game ID of the created game
                socket.emit('newMultiplayerGameCreated', gameId); // Emit the game ID to the client
            } catch (error) {
                console.error('Error creating multiplayer game:', error);
                socket.emit('error', 'Failed to create game. Please try again.');
            }
        });

        // Joining an existing multiplayer game
        socket.on('joinGameRequested', async (userId, gameId) => {
            try {
              console.log(`joinGameRequested: userId=${userId}, gameId=${gameId}`);
          
              // Call the joinGame function and await the result
              const joinedGameId = await lobbyManager.joinGame(userId, gameId);
          
              console.log('Game joined successfully:', joinedGameId);
          
              // Emit the joined game ID back to the client
              socket.emit('joinGameReplied', (joinedGameId));
            }
            catch (error) {
              console.error('Error joining game:', error.message);
          
              // Emit the error to the client
              socket.emit('joinGameReplied', (null));
            }
          });
        
        // Sync Boards
        socket.on('syncBoard', (gameId) => {
            syncBoard(socket, gameId);
        });

        // Making a move
        socket.on('move', (gameId, gameState) => {
            handleMove(io, socket, gameId, gameState);
        });

        // Handle disconnecting player
        socket.on('disconnect', async () => {
            const userId = socket.id;
            await lobbyManager.handleDisconnect(userId);
        });
    });
};


