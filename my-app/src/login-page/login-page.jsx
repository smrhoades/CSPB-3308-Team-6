import './login-page.css'

function LoginPage() {
    return (
        <div class="center-box">
            <h1>Welcome!</h1>
            <form>
                <label htmlFor="username">username</label>
                <br></br>
                <input type="text" id="username-input" name="username" className="login-input"></input>
                <br></br>
                <label htmlFor="password">password</label>
                <br></br>
                <input type="text" id="password-input" name="password" className="login-input"></input>
                <br></br>
                <button>login</button>
            </form>
        </div>
    )
}

export default LoginPage