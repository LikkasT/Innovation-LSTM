import Cookies from "js-cookie";

const userCookie = "userCookie";

// 获取用户信息
export function getUserCookie() {
    const admin = Cookies.get(userCookie);
    if (admin) {
        return JSON.parse(admin);
    }
    return ''
}

//存储用户信息
export function setUserCookie(admin) {
    console.log(JSON.stringify(admin));
    return Cookies.set(userCookie, JSON.stringify(admin))
}
//移除用户信息
export function removeUserCookie() {
    return Cookies.remove(userCookie)
}
