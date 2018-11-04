/**
 * Created by huangxinxin on 16/6/20.
 */
const utils = {}

utils.isStatusEqual = function (a, b) {
  if (a && b) {
    a = '' + a
    b = '' + b
    let v1 = a.split('@Time:')[ 0 ]
    let v2 = b.split('@Time:')[ 0 ]
    return v1 === v2
  }
  return false
}

utils.setStatus = function (state, keyStr, value) {
  let keyArr = keyStr.split('.')
  let lastKey = keyArr.pop()
  let status = state.status
  for (let i = 0; i < keyArr.length; i++) {
    let k = keyArr[ i ]
    if (status.hasOwnProperty(k)) {
      status = status[ k ]
    }
  }
  if (status.hasOwnProperty(lastKey)) {
    status[ lastKey ] = value + '@Time:' + (new Date().toLocaleString()) + '@Random: ' + (~~(Math.random() * Math.pow(10, 8)))
  }
}

export default utils
