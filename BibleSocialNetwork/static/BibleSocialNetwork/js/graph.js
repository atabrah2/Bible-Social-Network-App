var node = {
	x: 0,
	y: 0,
	radius: 10,
	inLink: false,
	createNode: function () {
		return Object.create(node);
	}
};
var edge = {
    startNode: null,
    endNode: null,
    inLink: false,
    createEdge: function () {
        return Object.create(edge);
    }
};
var Vector = {
	x: 0,
	y: 0,
	createVec: function(x, y) {
		var vec = Object.create(Vector);
		vec.x = x;
		vec.y = y;
		return vec;
	},
	vecLength: function () {
		return Math.sqrt(this.x * this.x + this.y * this.y);
	},
	vecAdd: function (v) {
		return Vector.createVec(this.x + v.x, this.y + v.y);
	}
};

var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

var linkHeight=10;
var linkWidth;
var N = 11;
var nodeList = [];
var edgeList = [];
var T = 10;
var edges = [];

function initialize() {
	for (var i = 0; i < N; i++){
		var n = node.createNode();
		a = Math.random();
		if(a < 0.3) {
		    a += 0.3;
		}
		if (a > 0.7) {
		    a -= 0.3;
		}
		b = Math.random();
		if (b < 0.3) {
		    b += 0.325
		}
		if (b > 0.6) {
		    b -= 0.325;
		}
		n.x = a * canvas.width;
		n.y = b * canvas.height;

		n.radius = 15;

		nodeList.push(n);
	}

	matrix= new Array();
	for (var i = 0; i < N; i++)
		matrix[i] = new Array(N);

	for (var i=0; i < 10; i++) {
	    var e = edge.createEdge();
	    e.startNode = nodeList[0];
        e.endNode = nodeList[i+1];
        edgeList.push([0,i+1]);
        edges.push(e);
    }
	for (var i = 0; i < edgeList.length; i++){
		matrix[edgeList[i][0]][edgeList[i][1]] = true;
		matrix[edgeList[i][1]][edgeList[i][0]] = true;
	}
}
var drawNode = function(ctx, x, y, rad, i) {

    ctx.fillStyle = "gray";
    ctx.strokeStyle = "black";
    ctx.beginPath();
    ctx.arc(x,y,rad,0,Math.PI*2);
    ctx.fill();
    ctx.stroke();
}
var drawEdge = function(ctx, x0, y0, x1, y1) {
    ctx.beginPath();
    ctx.moveTo(x0,y0);
    ctx.lineTo(x1,y1);
    ctx.stroke();
}
function draw(){
  canvas = document.getElementById("myCanvas");
  // check if supported
  if(canvas.getContext){
    ctx=canvas.getContext("2d");
	ctx.lineWidth = 2;
    ctx.strokeStyle = "#000000";
    for (var i = 0; i < edgeList.length; i++) {
        drawEdge(ctx, nodeList[edgeList[i][0]].x, nodeList[edgeList[i][0]].y, nodeList[edgeList[i][1]].x, nodeList[edgeList[i][1]].y);
    }
	for (var i = 0; i < N; i++){
	    drawNode(ctx, nodeList[i].x, nodeList[i].y, nodeList[i].radius, i);
	    //draw the link
        ctx.font='10px sans-serif';
        ctx.fillStyle = "#0000ff";
        ctx.fillText(i.toString(),nodeList[i].x-3,nodeList[i].y+3);
        linkWidth=ctx.measureText(i.toString()).width;
        //add mouse listeners
        canvas.addEventListener("mousemove", on_mousemove, false);
        canvas.addEventListener("click", on_click, false);
	}
  }
}
function getLocalMousePos(canvas, ev) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: ev.clientX - rect.left,
        y: ev.clientY - rect.top
    };
}
function on_mousemove (ev) {
    var localMouse = getLocalMousePos(canvas, ev);
    document.body.style.cursor = "";
    var xoff = 300;
    for (var i = 0; i < nodeList.length; i++) {
        if (Math.sqrt(Math.pow(nodeList[i].x-localMouse.x+xoff, 2)+Math.pow(nodeList[i].y-localMouse.y, 2)) < nodeList[i].radius) {
            document.body.style.cursor = "pointer";
            nodeList[i].inLink = true;
            console.log("collision with node "+i);
        }
        else {
            nodeList[i].inLink = false;
        }
    }
    for (var i = 0; i < edges.length; i++) {
        var xmid = (edges[i].endNode.x + edges[i].startNode.x)/2.0;
        var ymid = (edges[i].endNode.y + edges[i].startNode.y)/2.0;
        if (localMouse.x-xoff < xmid + 5 && localMouse.x-xoff > xmid - 5 && localMouse.y < ymid + 5 && localMouse.y > ymid - 5) {
            document.body.style.cursor = "pointer";
            edges[i].inLink = true;
            console.log("collision with edge "+i);
        }
        else {
            edges[i].inLink = false;
        }
    }
}
//if the link has been clicked, go to link
function on_click(e) {
    for (var i = 0; i < nodeList.length; i++) {
        if (nodeList[i].inLink) {
            var test3 = "You clicked node " + i.toString();
            document.getElementById("mytext3").value = test3;
            document.getElementById("myBtn").click();
        }
    }
    for (var i = 0; i < edges.length; i++) {
        if (edges[i].inLink) {
            var test3 = "You clicked edge " + i.toString();
            document.getElementById("mytext3").value = test3;
            document.getElementById("myBtn").click();
        }
    }
}
//Hooke's Law spring attraction
function HookeAttract(i, j) { // the result can be direct added to i
	var K = 0.1; //arbitrary spring constant, corresponds with Coulomb's constant
	var L = 20; //displaced (max) length
	if(!matrix[i][j]) {
        return Vector.createVec(0, 0);
	}
	var diff = Vector.createVec(nodeList[i].x - nodeList[j].x, nodeList[i].y - nodeList[j].y);
	var len = diff.vecLength(); //distance between nodes or resting position of spring
	var norm = Vector.createVec(diff.x/len, diff.y/len);
	return Vector.createVec(norm.x * (K * (L - len)), norm.y * (K * (L - len)));
}
//Coulomb's Law - electrical repulsion between nodes
function CoulombRepel(i, j) {   // the result can be direct added to i

    var K = 18000; //arbitrary Coulomb's constant equivalent, corresponds with spring constant

	var diff = Vector.createVec(nodeList[i].x - nodeList[j].x, nodeList[i].y - nodeList[j].y);
	var len = diff.vecLength();
	var norm = Vector.createVec(diff.x/len, diff.y/len); //distance between nodes
	return  Vector.createVec(norm.x * (K / Math.pow(len,2)), norm.y * (K / Math.pow(len,2)));
}
function redraw(){
	ctx.clearRect(0, 0, 800, 600);
	var move = new Array(N);
	for (var i = 0; i < N; i++) {
	    move[i] = Vector.createVec(0, 0);
	}
	for (var i = 0; i < N; i++) {
	    for (var j = i + 1; j < N; j++){
			var v1= HookeAttract(i, j).vecAdd(CoulombRepel(i, j)); //endpoint attraction and node repulsion combined
			move[i] = move[i].vecAdd(v1); //attract
			var neg = Vector.createVec(-(v1.x), -(v1.y));
			move[j] = move[j].vecAdd(neg); //repel
		}
	}
	for (var i = 0; i < N; i++){
		nodeList[i].x += move[i].x;
		nodeList[i].y += move[i].y;
	}
	draw();
}
initialize();
setInterval(redraw,50);