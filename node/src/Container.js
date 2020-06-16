module.exports = class Container {

  constructor() {
    this.instances = {}
  }

  get(name) {
    return this.instances[name]
  }

  has(name) {
    return this.instances[name] !== undefined
  }

  set(name, value) {
    this.instances[name] = value
  }
}