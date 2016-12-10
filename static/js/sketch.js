var img;
var imgwidth, imgheight;
var topstr, bottomstr;
var topSize, bottomSize;
var topStroke, bottomStroke;
var topLines, bottomLines;

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
    
    //topLines = topstr.value().match(/.{1,15}/g);
    /*size = 15;
      topLines = topstr.value().match(new RegExp('.{1,' + size + '}', 'g'));*/
    topLines = split_line(topstr.value(), 4);
    console.log(topLines);
    if (topLines != null && topLines.length > 0) {
	topSize = width/(topLines[0].length + topLines.length) * max((img.height/img.width), (img.width/img.height));
	if(topSize > height/2) { topSize = height/2; }
	textSize(topSize * 1.5);
	strokeWeight(topSize/20);
	for(i = 0; i < topLines.length; i++) {
	    text(topLines[i], width/2, (topSize * 1.5)/4*3 * (i+1));
	}
    }
    
    bottomLines = split_line(bottomstr.value(), 4);
    //bottomLines = bottomstr.value().match(/.{1,15}/g);
    if (bottomLines != null && bottomLines.length > 0) {
	bottomSize = width/(bottomLines[0].length + bottomLines.length) * max((img.height/img.width), (img.width/img.height));
	if(bottomSize > height/2) {bottomSize = height/2;}
	textSize(bottomSize);
	strokeWeight(bottomSize/20);
	for(i = bottomLines.length - 1; i >= 0; i--) {
	    text(bottomLines[bottomLines.length - i - 1], width/2, height - bottomSize/4*3 * (i+1));
	}

    }
}

function split_line(string, step) {
    var words = string.split(" ");
    var strings = [];
    var line = "";
    for (i in range(words.length)) {
	line += words[i] + " ";
	if ( i % step == step-1) {
	    strings.push(line);
	    line = "";
	} 
    }

    return strings;
}

function range(val) {
    var range = [];
    for (i = 0 ; i < val; i++) {
	range.push(i);
    }
    return range;
}
/*def split_lines(s, step):
    words = s.split()
    firsthalf = ""
    secondhalf = ""
    upper = 0
    for i in range(int(math.ceil(len(words)/2.0))):
        firsthalf += words[upper] + " "
        upper += 1
    for i in range(int(math.floor(len(words)/2.0))):
        
    splits = [firsthalf, secondhalf]
    return splits*/
