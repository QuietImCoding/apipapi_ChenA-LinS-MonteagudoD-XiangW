var img;
var imgwidth, imgheight;
var topstr, bottomstr;

function preload() {
    img = loadImage(select("#url").value());
}

function setup() {

    imgwidth = img.width;
    imgheight = img.height;
    var canvas = createCanvas(imgwidth, imgheight);
    canvas.parent('meme-holder');
    textAlign(CENTER, CENTER);
    textSize(50);
    topstr = select("#top");
    bottomstr = select("#bottom");
}

function draw() {
    stroke(0);
    fill(255);
    image(img, 0, 0);
    var topSize = width/topstr.value().length * 2;
    var bottomSize = width/bottomstr.value().length * 2;
    var topStroke = topSize/20;
    var bottomStroke = bottomSize/20;
    textSize(topSize);
    strokeWeight(topStroke);
    text(topstr.value(), width/2, topSize/2);
    textSize(bottomSize);
    strokeWeight(bottomStroke);
    text(bottomstr.value(), width/2, height-bottomSize/2);
}
