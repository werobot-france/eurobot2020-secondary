var gpio = require("gpio");
var gpio4 = gpio.export(20, {
   direction: gpio.DIRECTION.IN,
   ready: function() {
   }
});
gpio4.on('change', (val) => {
  console.log(val)
})
var gpio_ = gpio.export(16, {
  direction: gpio.DIRECTION.IN,
  ready: function() {
  }
});
gpio_.on('change', (val) => {
 console.log(val)
})
var gpio_1 = gpio.export(6, {
  direction: gpio.DIRECTION.IN,
  ready: function() {
  }
});
gpio_1.on('change', (val) => {
 console.log(val)
})