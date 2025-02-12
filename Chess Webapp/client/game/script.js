// --------------------------------
// Chess Initialization
// --------------------------------

// Connect to the server
const socket = io();

//Get Game ID
const path = window.location.pathname;
const gameId = path.split('/')[2];
const gameIdValue = document.getElementById('game-id-value');

// Get user ID
const userId = localStorage.getItem('userId');
if (!userId) {
  console.error('User ID not found in local storage');
}

// Initialize game ID label
if (gameId && gameIdValue) {
  gameIdValue.textContent = gameId;
} else {
  console.error('Game ID not found in URL or element missing!');
}



// --------------------------------
// Client Side Chess Board
// --------------------------------

// Game state variables
let pieceSet = 'lichess';
let userInteracted = false;
let isPromotionModalOpen = false;
let myColor = null;
let isTurn = null;
let gameHasStarted = false;
let $status = $('#status')
let $fen = $('#fen')
let $pgn = $('#pgn')
let $gameId = $('#game-id')
let gameOver = false;
let whiteSquareGrey = '#a9a9a9'
let blackSquareGrey = '#696969'

const icons = {
  light: '../img/copyicon/copy-icon-light.png',
  dark: '../img/copyicon/copy-icon-dark.png'
};


// Board settings
let config = {
  draggable: true,
  position: 'start',
  orientation: 'white',
  showNotation: false,
  dropOffBoard: 'snapback',
  pieceTheme: `../img/chesspieces/${pieceSet}/{piece}.png`,
  onDragStart: onDragStart,
  onDrop: onDrop,
  onMouseoutSquare: onMouseoutSquare,
  onMouseoverSquare: onMouseoverSquare,
  onSnapEnd: onSnapEnd
};

// Preload sounds
const sounds = {
  move: new Audio('/audio/lichess/move.mp3'),       // Absolute path for "move" sound
  capture: new Audio('/audio/lichess/capture.mp3'), // Absolute path for "capture" sound
  promotion: new Audio('/audio/chesscom/promote.webm'), // Absolute path for "promotion" sound
  check: new Audio('/audio/chesscom/check.webm'),   // Absolute path for "check" sound
  castle: new Audio('/audio/chesscom/castle.webm'), // Absolute path for "castle" sound
  checkmate: new Audio('/audio/chesscom/check.webm') // Absolute path for "checkmate" sound
};

// Create a chess board with configuration above
let board = Chessboard('myBoard', config);
let game = new Chess();




// --------------------------------
// Game Setup Request
// --------------------------------

// Notify the server to start tracking board activity
socket.emit('userConnected', userId, gameId);


// -------------------------------
// Socket Events
// -------------------------------

//Listen for team from the server
socket.on('teamAssignment', (team) => {
  teamAssignment(team);
});

// Listen for the turnAssignment event from the server
socket.on('currentTurn', (currentTurn) => {
  turnAssignment(currentTurn); 
});

// Sync the board with the server's FEN
socket.on('syncBoard', (serverGameState) => {
  syncBoard(serverGameState);
});

// Listen for the updateBoard event from the server
socket.on('updateBoard', (fen) => {
  game.load(fen);
  board.position(fen);
  updateStatus();
});

// Receive turn change
socket.on('notifyTurn', (turn) => {
  notifyTurn(turn);
});

// Receive outcome change
socket.on('outcomeChange', (outcome) => {
  $status.text(outcome);
});

// Listen for the opponent's move
socket.on('opponentMove', (move) => {
  game.move(move); // Make the move
  board.position(game.fen()); //Update the board position
  playSound(move); // Play the corresponding sound
  updateStatus(); //Update the game status
});


// -------------------------------
// Socket Functions
// -------------------------------

//Assign the user a team
function teamAssignment(team) {
  myColor = team;
  config.orientation = team;
  board = Chessboard('myBoard', config);
}

//Assign the user a turn
function turnAssignment(currentTurn) {
  if (!myColor) {
    console.error('Color not assigned yet');
    return;
  }
  isTurn = (myColor === 'white' && currentTurn === 'w') || (myColor === 'black' && currentTurn === 'b');
}


//Notify change in turn 
function notifyTurn(turn) {
  isTurn = (myColor === 'white' && turn === 'w') || (myColor === 'black' && turn === 'b');
}

// Sync the board with the server's 
function syncBoard(serverGameState) {
  const gameState = serverGameState;
  turnAssignment(gameState.turn);
    
  if (!serverGameState || !gameState.fen || !gameState.pgn) {
    return;
  }

  try {
    game.load(gameState.fen);
    board.position(game.fen);
    
    // Dynamically update the content of FEN and Status divs
    document.getElementById('fen').innerText = gameState.fen || ''; // Placeholder text
    document.getElementById('status').innerText = gameState.outcome || 'Game in Progress';  // Placeholder text
    document.getElementById('pgn').innerText = gameState.pgn || ''; // Placeholder text
  }
  catch (error) {
    //Error msgs
    console.error('Error loading position:', error);
    console.log('Attempted to load FEN:', gameState.fen);
    console.log('Attempted to load PGN:', gameState.pgn);

    // Handle errors by updating the status
    document.getElementById('status').innerText = 'Error loading position';
    document.getElementById('fen').innerText = 'Invalid FEN';
    document.getElementById('pgn').innerText = 'Invalid PGN';
  }
}

// Request a board sync from the server 
function requestBoardSync() {
  socket.emit('requestBoardSync'); // Request a board sync
}


// Determine which sound to play
function getSoundForMove(move) {
  if (move == null) {
    return 'error'; // Invalid move
  }
  else if (move.captured) {
      return 'capture'; // Capturing a piece
  } else if (move.promotion) {
      return 'promotion'; // Pawn promotion
  } else if (game.in_checkmate() || game.in_check()) {
      return 'check'; // Checkmate
  } else if (move.from === 'e1' && move.to === 'g1' || move.from === 'e8' && move.to === 'g8' || move.from === 'e1' && move.to === 'c1' || move.from === 'e8' && move.to === 'c8') {
      return 'castle'; // Castling
  }
  return 'move'; // Regular move
}

function playSound(move) {
  const sound = getSoundForMove(move);

  if (!userInteracted) {
    console.warn('User has not interacted with the page yet. Sound will not play.');
    return;
  }

  switch (sound) {
    case 'move':
      sounds.move.play().catch(error => console.error('Error playing move sound:', error));
      break;
    case 'capture':
      sounds.capture.play().catch(error => console.error('Error playing capture sound:', error));
      break;
    case 'promotion':
      sounds.promotion.play().catch(error => console.error('Error playing promotion sound:', error));
      break;
    case 'check':
      sounds.check.play().catch(error => console.error('Error playing check sound:', error));
      break;
    case 'castle':
      sounds.castle.play().catch(error => console.error('Error playing castle sound:', error));
      break;
    case 'checkmate':
      sounds.checkmate.play().catch(error => console.error('Error playing checkmate sound:', error));
      break;
    case 'error':
      console.warn('Invalid move. Sound will not play.');
      break;
    default:
      console.warn('Unknown sound:', sound);
  }
}

// Send the move to the server
function sendMoveToServer(gameId, gameState) {
  socket.emit('move', gameId, gameState); // Emit the move to the server
}

// Function to change piece theme
function changePieceSet(set) {
  const newPieceTheme = `../img/chesspieces/${set}/{piece}.png`;

  // Update the chessboard
  config.pieceTheme = newPieceTheme;
  board = Chessboard('myBoard', config);
  // Request a board sync from the server
  requestBoardSync();

  // Update Promotion Modal
  updatePromotionModal(set);
}

// Function to set the userInteracted flag
function setUserInteracted() {
  userInteracted = true;
  // Remove the event listeners after the first interaction to avoid unnecessary checks
  document.removeEventListener('click', setUserInteracted);
}
  
function checkOutcome(game) {
  let outcome = '';
  // Checkmate?
  if (game.in_checkmate()) {
    outcome = 'checkmate';
  }
  // Draw?
  else if (game.in_draw()) {
    outcome = 'draw';
  }
  else {
    outcome = 'ongoing';
  }
  return outcome;
}









// -------------------------------
// Legal Moves
// -------------------------------

// Function for handling drag events
function onDragStart(source, piece, position, orientation) {
    // Do not pick up pieces if the game is over
    if (game.game_over() || isPromotionModalOpen) return false;
  
    //Do not allow interaction if not the player's turn
    if (!isTurn) return false;
  
    // Prevent picking up opponent's pieces
    if ((myColor === 'black' && piece.search(/^w/) !== -1) || 
        (myColor === 'white' && piece.search(/^b/) !== -1)) {
      return false;
    }
  
    return true;
  }
  
// Function for handling drop events
async function onDrop(source, target) {
  
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  //Prevent dropping if promotion modal is open
  if (isPromotionModalOpen) return 'snapback';
  
  // Remove grey squares
  removeGreySquares();

  // Check if the move is a pawn reaching the promotion rank
  const piece = game.get(source).type; // Get the piece type
  const promotionRank = target.endsWith('8') || target.endsWith('1'); // Check rank


  let promotion = 'q'; // Default to queen

  //Handle promotion
  if (piece === 'p' && promotionRank) {
    let validPromotionSelected = false;

    // Loop until a valid promotion choice is made or the user cancels
    while (!validPromotionSelected) {
      try {
        // Wait for the user to select a promotion piece (or cancel)
        promotion = await openPromotionModal(); // This will resolve with the selected piece or reject on cancel
        validPromotionSelected = true; // If a valid selection is made, exit the loop
      } catch (reason) {
        // Handle the cancelation (if the user pressed Escape)
        if (reason === 'cancel') {
          return 'snapback'; // Return 'snapback' to reset the piece position or cancel the move
        }
      }
    }
  }

  // Now that the promotion piece is selected, proceed with the move
  const move = game.move({
    from: source,
    to: target,
    promotion: promotion
  });
  
  // If the move is illegal, snap the piece back
  if (move === null) return 'snapback';

  //Play corresponding sound
  playSound(move);

  // Update the website labels
  updateStatus();

  // Check outcome of the game
  outcome = checkOutcome(game);
  gameStateObject = {
    turn: game.turn(),
    fen: game.fen(),
    pgn: game.pgn(),
    outcome: outcome,
    move: move
  };
  
  // Otherwise, send the move to the server
  sendMoveToServer(gameId, gameStateObject);
}

// Finalize the move visually
function onSnapEnd() {
  board.position(game.fen());
}

// Function to update the status of the game
function updateStatus () {
  var status = ''

  var moveColor = 'White'
  if (game.turn() === 'b') {
    moveColor = 'Black'
  }

  // checkmate?
  if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  }

  // draw?
  else if (game.in_draw()) {
    status = 'Game over, drawn position'
  }

  // game still on
  else {
    status = moveColor + ' to move'

    // check?
    if (game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }

  $status.html(status) // Update the status label
  $fen.html(game.fen()) // Update the FEN label
  $pgn.html(game.pgn()) // Update the PGN label
  $gameId.html(gameId) // Update the game ID label
}


  
  






  // -------------------------------
  // Highlight Legal Moves
  // -------------------------------
  
  // Remove the grey squre highlights
  function removeGreySquares() {
    $('#myBoard .square-55d63').css('background', '');
  }
  
  // Highlight the possible moves for the selected piece
  function greySquare(square) {
    let $square = $('#myBoard .square-' + square);
    let background = whiteSquareGrey;
    if ($square.hasClass('black-3c85d')) {
      background = blackSquareGrey;
    }
    $square.css('background', background);
  }
  
  // Highlight the possible moves for the selected piece
  function onMouseoverSquare(square, piece) {
    // Only proceed if it's the current player's turn
    if (!isTurn || isPromotionModalOpen) return;
  
    // Get the color of the piece (first character of the piece type)
    if (piece === false) return;
  
    let pieceColor = piece.charAt(0); // 'w' for white, 'b' for black
  
    // Only highlight moves if the piece belongs to the current player
    if ((myColor === 'white' && pieceColor === 'w') || (myColor === 'black' && pieceColor === 'b')) {
      // Get the list of legal moves for this square
      let moves = game.moves({
          square: square,
          verbose: true
      });
  
      // Exit if there are no legal moves available for this square
      if (moves.length === 0) return;
  
      // Highlight the square they moused over
      greySquare(square);
  
      // Highlight the possible squares for this piece
      for (let i = 0; i < moves.length; i++) {
          greySquare(moves[i].to);
      }
    }
  }
  
  // Remove the highlights of possible moves for the selected piece
  function onMouseoutSquare (square, piece) {
    removeGreySquares()
  }
  
  
//---------------------------
// Event Listeners
//---------------------------

// Set the flag when the user clicks or moves the mouse
document.addEventListener('click', setUserInteracted);

//Sync board on reconnection
window.addEventListener('load', () => {
  socket.emit('requestBoardSync');
});

// Call loadTheme when page loads
document.addEventListener('DOMContentLoaded', loadTheme);


  

// -------------------------------
// Webpage Widget Functionality
// -------------------------------

// Theme Switching
document.getElementById('lightTheme').addEventListener('click', () => {
    document.body.removeAttribute('data-theme');
    updateActiveThemeButton('lightTheme');
    localStorage.setItem('theme', 'light');
  });

document.getElementById('darkTheme').addEventListener('click', () => {
  document.body.setAttribute('data-theme', 'dark');
  updateActiveThemeButton('darkTheme');
  localStorage.setItem('theme', 'dark');
});

// Update copy button image based on the theme
function updateCopyButtonImage(theme) {
  const copyButtons = document.querySelectorAll('.copy-btn img');
  const icon = theme === 'dark' ? icons.dark : icons.light;

  copyButtons.forEach(button => {
    button.src = icon;
  });
}

// Call updateCopyButtonImage when the theme changes
document.getElementById('lightTheme').addEventListener('click', () => {
  updateCopyButtonImage('light');
});

document.getElementById('darkTheme').addEventListener('click', () => {
  updateCopyButtonImage('dark');
});

// Update the copy button image when the page loads
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  updateCopyButtonImage(savedTheme === 'dark' ? 'dark' : 'light');
});
function updateActiveThemeButton(activeId) {
  document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.remove('active');
  });
  document.getElementById(activeId).classList.add('active');
}

// Load saved theme preference
function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
      document.body.setAttribute('data-theme', 'dark');
      updateActiveThemeButton('darkTheme');
  }
}

// FEN copy functionality
document.getElementById('copyFen').addEventListener('click', () => {
  const fen = game.fen();
  navigator.clipboard.writeText(fen).then(() => {
      const btn = document.getElementById('copyFen');
      btn.textContent = 'Copied!';
      setTimeout(() => {
          btn.textContent = 'Copy FEN';
      }, 2000);
  }).catch(err => {
      console.error('Failed to copy FEN:', err);
  });
});

// PGN copy functionality
document.getElementById('copyPgn').addEventListener('click', () => {
  const pgn = document.getElementById('pgn').innerText;
  navigator.clipboard.writeText(pgn).then(() => {
      const btn = document.getElementById('copyPgn');
      btn.textContent = 'Copied!';
      setTimeout(() => {
          btn.textContent = 'Copy PGN';
      }, 2000);
  }).catch(err => {
      console.error('Failed to copy PGN:', err);
  });
});

// Game ID Copy Functionality
document.getElementById('copyGameId').addEventListener('click', () => {
  const gameId = document.getElementById('game-id').innerText;
  navigator.clipboard.writeText(gameId).then(() => {
      const btn = document.getElementById('copyGameId');
      btn.textContent = 'Copied!';
      setTimeout(() => {
          btn.textContent = 'Copy Game ID';
      }, 2000);
  }).catch(err => {
    console.error('Failed to copy Game ID:', err);
  });
});

// Change piece set to Lichess
document.getElementById('lichess-btn').addEventListener('click', () => {
  changePieceSet('lichess');
});

// Change piece set to Chess.com
document.getElementById('chesscom-btn').addEventListener('click', () => {
  changePieceSet('chesscom');
});

// Function to open the promotion modal and return the selected piece
function openPromotionModal() {
  return new Promise((resolve, reject) => {
    // Show the modal
    document.getElementById('promote-modal').style.display = 'block';

    // Set the flag to true
    isPromotionModalOpen = true;

    // Store the resolve and reject functions in global variables
    window.promotionResolve = resolve;
    window.promotionReject = reject;

    // Add event listener to close the modal if the user presses Escape
    document.addEventListener('keydown', handleEscapeKey, { once: true });
  });
}

// Function to handle pressing the Escape key
function handleEscapeKey(event) {
  // If the Escape key is pressed and no promotion piece has been selected, reject the promotion
  if (event.key === 'Escape') {
    closePromotionModal('cancel');
  }
}

// Function to close the promotion modal
function closePromotionModal(reason) {
  // Close the modal
  document.getElementById('promote-modal').style.display = 'none';

  // Set the flag to false
  isPromotionModalOpen = false; // Correctly set the flag to false

  // Reject or resolve the promise if applicable
  if (reason === 'cancel' && typeof window.promotionReject === 'function') {
    window.promotionReject(reason);
    window.promotionReject = null; // Clear the reject function after use
  }

  // Remove event listeners to avoid memory leaks
  document.removeEventListener('keydown', handleEscapeKey);
}

// Function to handle the promotion choice (user clicks a button)
function selectPromotion(piece) {
  // Close the modal
  document.getElementById('promote-modal').style.display = 'none';

  // Set the flag to false
  isPromotionModalOpen = false; // Correctly set the flag to false

  // Resolve the promise with the selected promotion piece (q, r, b, n)
  if (typeof window.promotionResolve === 'function') {
    window.promotionResolve(piece);
    window.promotionResolve = null; // Clear the resolve function after use
  }

  // Remove event listeners to avoid memory leaks
  document.removeEventListener('keydown', handleEscapeKey);
}

// Update promotion modal with new piece set
function updatePromotionModal(set) {
  const promotionButtons = document.querySelectorAll('.promotion-btn');
  const isWhite = config.orientation === 'white';

  // Update the image source based on the orientation (white or black)
  promotionButtons.forEach(button => {
    const pieceType = button.querySelector('img').alt.charAt(0);
    const pieceColor = isWhite ? 'w' : 'b';
    const newImageSrc = `../img/chesspieces/${set}/${pieceColor}${pieceType}.png`; // Adjust this to match your image naming convention
    button.querySelector('img').src = newImageSrc;
  });
};