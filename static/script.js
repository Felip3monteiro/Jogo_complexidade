function startGame() {
    fetch('/start-game')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function quitGame() {
    alert("Saindo do jogo...");
    window.close();
}