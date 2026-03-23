export default function LoginForm({ credentials, setCredentials, onLogin }) {
  return (
    <div className="login">
      <form>
        <h2>LOGIN</h2>

        <input
          placeholder="USERNAME"
          value={credentials.username}
          onChange={(e) =>
            setCredentials({ ...credentials, username: e.target.value })
          }
        />

        <input
          type="password"
          placeholder="PASSWORD"
          value={credentials.password}
          onChange={(e) =>
            setCredentials({ ...credentials, password: e.target.value })
          }
        />

        <button type="button" onClick={onLogin}>
          LOGIN
        </button>
      </form>
    </div>
  );
}