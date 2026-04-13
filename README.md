# MO-302-Simulation-Game-
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Track League Negotiation Simulator</title>
<style>
    body { font-family: Arial; background: #111; color: #fff; text-align: center; }
    .container { max-width: 800px; margin: auto; padding: 20px; }
    button { margin: 10px; padding: 10px 20px; font-size: 16px; cursor: pointer; }
    .metrics { display: flex; justify-content: space-around; margin: 20px 0; }
    .box { padding: 10px; background: #222; border-radius: 10px; }
</style>
</head>
<body>

<div class="container">
    <h1>🏁 Track League Negotiation Simulator</h1>

    <div class="metrics">
        <div class="box">Trust: <span id="trust"></span></div>
        <div class="box">Investors: <span id="investors"></span></div>
        <div class="box">Athletes: <span id="athletes"></span></div>
        <div class="box">Debt: $<span id="debt"></span></div>
    </div>

    <h2 id="round"></h2>

    <input type="number" id="offerInput" placeholder="Enter offer" />
    <br>

    <button onclick="makeOffer()">Make Offer</button>
    <button onclick="askQuestions()">Ask Questions</button>
    <button onclick="packageDeal()">Package Deal</button>
    <button onclick="appealAthletes()">Appeal Athletes</button>
    <button onclick="appealInvestors()">Appeal Investors</button>
    <button onclick="walkAway()">Walk Away</button>

    <h3 id="output"></h3>
</div>

<script>
let game = {
    leagueValue: Math.floor(Math.random()*7000000)+8000000,
    trueMin: 0,
    debt: 40680000,
    trust: 50,
    investors: 50,
    athletes: 50,
    round: 1,
    maxRounds: 6,
    deal: false
};

game.trueMin = Math.floor(game.leagueValue * (Math.random()*0.25 + 0.7));

function updateUI(){
    document.getElementById("trust").innerText = game.trust;
    document.getElementById("investors").innerText = game.investors;
    document.getElementById("athletes").innerText = game.athletes;
    document.getElementById("debt").innerText = game.debt.toLocaleString();
    document.getElementById("round").innerText = "Round " + game.round;
}

function evaluate(offer){
    let score = 0;

    if(offer >= game.trueMin) score += 40;
    else if(offer >= game.trueMin*0.85) score += 25;
    else score += 10;

    score += game.trust*0.2;
    score += game.investors*0.2;
    score += game.athletes*0.2;

    if(game.debt > 30000000) score -= 20;

    return score;
}

function makeOffer(){
    let offer = parseInt(document.getElementById("offerInput").value);
    let score = evaluate(offer);

    if(score > 80){
        game.deal = true;
        output("Deal Accepted! You win.");
    }
    else if(score > 60){
        let counter = Math.floor((offer + game.trueMin)/2);
        game.trust += 5;
        output("Counteroffer: $" + counter.toLocaleString());
    }
    else{
        game.trust -= 10;
        output("Offer Rejected");
    }

    nextRound();
}

function askQuestions(){
    game.trust += 10;
    game.investors += 5;
    output("You gathered valuable intel.");
    nextRound();
}

function packageDeal(){
    if(Math.random() > 0.4){
        let reduction = Math.floor(Math.random()*7000000)+8000000;
        game.debt -= reduction;
        game.trust += 10;
        output("Debt reduced by $" + reduction.toLocaleString());
    } else {
        game.trust -= 5;
        output("Package rejected.");
    }
    nextRound();
}

function appealAthletes(){
    game.athletes += 15;
    game.trust += 5;
    output("Athletes support increased.");
    nextRound();
}

function appealInvestors(){
    game.investors += 15;
    game.trust += 5;
    output("Investor confidence increased.");
    nextRound();
}

function walkAway(){
    if(Math.random() > 0.4){
        output("You walked away and built a successful league.");
    } else {
        output("Your new league failed.");
    }
}

function nextRound(){
    updateUI();
    if(game.deal) return;

    game.round++;
    if(game.round > game.maxRounds){
        output("Negotiation ended. No deal.");
    }
}

function output(msg){
    document.getElementById("output").innerText = msg;
}

updateUI();
</script>

</body>
</html>

