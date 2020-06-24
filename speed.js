let generate = (angle, speed ) => {

  let generateCoeffs = (a) => {
    return Math.cos(Math.abs(angle*Math.PI/180 - a*Math.PI/180))
  }

  let eastCoef       =  generateCoeffs(-90)
  //let northEastCoef  =  generateCoeffs(-45)
  let northCoef      =  generateCoeffs(0)
  //let northWestCoef  =  generateCoeffs(45)
  let westCoef       =  generateCoeffs(90)
  //let southWestCoef  =  generateCoeffs(135)
  let southCoef      =  generateCoeffs(180)
  //let southEastCoef  =  generateCoeffs(-135)
  
  // let east =      [eastCoef, eastCoef, eastCoef, eastCoef]
  // let northEast = [northEastCoef, 0, 0, northEastCoef]
  // let north =     [northCoef, -northCoef, -northCoef, northCoef]
  // let northWest = [0, northWestCoef, northWestCoef, 0]
  // let west =      [-westCoef, -westCoef, -westCoef, -westCoef]
  // let southWest = [-southWestCoef, 0, 0, -southWestCoef]
  // let south =     [-southCoef, southCoef, southCoef, -southCoef]
  // let southEast = [0, -southEastCoef, -southEastCoef, 0]

  let cmds = [
    [eastCoef, eastCoef, eastCoef, eastCoef],
    //[northEastCoef, 0, 0, northEastCoef],
    [northCoef, -northCoef, -northCoef, northCoef],
    //[0, northWestCoef, northWestCoef, 0],
    [-westCoef, -westCoef, -westCoef, -westCoef],
    //[-southWestCoef, 0, 0, -southWestCoef],
    [-southCoef, southCoef, southCoef, -southCoef],
    //[0, -southEastCoef, -southEastCoef, 0]
  ]

  let motorsSpeed = []
  for (var n = 0; n < 4; n++) {
    let sum = 0
    for (var i = 0; i < cmds.length; i++) {
      sum += cmds[i][n] * speed
    }
    motorsSpeed.push(parseFloat((sum / cmds.length * 2).toFixed(3)))
  }
  
  return (motorsSpeed)
}

console.log(generate(45, 1))