export function getUserToken() {
    return localStorage.getItem('token');
}

export function setUserToken(token: string) {
    localStorage.setItem('token', token);
}