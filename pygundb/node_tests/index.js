var Gun = require('gun')
require('gun/lib/unset')

var gun = Gun("ws://127.0.0.1:8000/gun")

let basicTest = () => {
    console.log("basic test.")
    gun.get("proj.simple://1").put({
      "attr1": "val"
    })
    gun.get("proj.simple://2").put({
      "attr2": 5
    })
    gun.get("proj.simple://2").put({
      "attr2": "zc"
    }) // should fail.

  }

  let midTest = () => {
    console.log("mid test")

    gun.get("proj.person://4").put({
      name: "ahmed"
    })
    gun.get("proj.person://4").put({
      "name": "ahmed"
    })
    gun.get("proj.person://4").get("email").put({
      "addr": "ahmed@gmail.com",
    })
    gun.get("proj.person://5").get("email").put({
      "addr": "andrew@gmail.com",
    })
    gun.get("proj.person://5").get("email").put({
      "addr": "dmdm@gmail.com",
    })
    gun.get("proj.person://5").get("email").put({
      "addr": "notdmdm@gmail.com",
    })

  }


  let advTest = () => {
    console.log("advanced test")
    gun.get("proj.human://7").put({
      "name": "xmon"
    })
    gun.get("proj.human://7").get("phone").put({
      "model": "samsung"
    })
    gun.get("proj.human://7").get("phone").get("os").put({
      "name": "android"
    })

    gun.get("proj.human://8").put({
      "name": "richxmon"
    })
    gun.get("proj.human://8").get("phone").put({
      "model": "iphone"
    })
    gun.get("proj.human://8").get("phone").get("os").put({
      "name": "ios"
    })
    gun.get("proj.human://8").get("list_favcolors").set("white")
    gun.get("proj.human://8").get("list_favcolors").set("red")
    gun.get("proj.human://8").get("list_favcolors").set("blue")
    // gun.get("proj.human://8").get("list_favcolors").unset("red")
    let python = gun.get('langs_python').put({name:'python'})
    gun.get("proj.human://8").get("list_langs").set(python)
    let ruby = gun.get('langs_ruby').put({name:'ruby'})
    gun.get("proj.human://8").get("list_langs").set(ruby)

  }
  let nesetedListTest = () => {
    // gun.get("proj.programmar://8").get("list_langs").set({
    //     "name": "python",
    //     "list_releases": {
    //     "0": "3.6",
    //     "1": "3.7"
    //     }
    // })
  }
//   for (let x=0; x < 5; x++){
    basicTest()
    midTest()
    advTest()
    nesetedListTest()
//   }
