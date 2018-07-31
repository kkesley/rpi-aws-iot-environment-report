const main = require('./handler').main
main({}, {}, (err, data) => {
    console.log(err)
    console.log(data)
})