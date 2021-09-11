<template>
  <div id="login">
    <div class="form-container">
      <div v-show="inputLabelVisible" class="invalid-password-label">
        パスワード違うし
      </div>
      <div class="password-forms">
        <input v-model="userName" placeholder="なまえ" type="text" />
        <input
          v-model="password"
          @keyup.enter="onClickSubmitButton"
          placeholder="パスワード"
          type="password"
        />
        <button @click="onClickSubmitButton">OK</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    token: {
      get() {
        return this.$store.state.token;
      },
      set(newValue) {
        this.$store.state.token = newValue;
      },
    },
    userName: {
      get() {
        return this.$store.state.userName;
      },
      set(newValue) {
        this.$store.state.userName = newValue;
      },
    },
    webSocketUrl: {
      get() {
        return this.$store.state.webSocketUrl;
      },
    },
  },
  created() {
    console.log("creating login component..");
    if (this.socket === null) {
      this.initializeWebSocket();
    }
    if (this.token) {
      this.socket.send(
        JSON.stringify({
          action: "validateToken",
          data: {
            token: this.token,
          },
        })
      );
    }
  },
  data() {
    return {
      inputLabelVisible: false,
      okButtonEnabled: false,
      password: "",
      socket: null,
    };
  },
  methods: {
    initializeWebSocket() {
      console.log("initializing websocket on login component..");
      this.socket = new WebSocket(this.webSocketUrl);
      this.socket.onopen = (e) => {
        console.log(e);
      };
      this.socket.onmessage = (e) => {
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        if (parsedData.dataType === "newToken") {
          // パスワードが承認され、新たにトークンが発行された場合
          this.token = parsedData.data.token;
          this.$router.push("/chat");
          return;
        } else if (parsedData.dataType === "validToken") {
          // トークンが正しいと承認された場合
          this.$router.push("/chat");
          return;
        } else if (parsedData.dataType === "invalidPassword") {
          // パスワードが違った場合
          this.inputLabelVisible = true;
          return;
        } else if (parsedData.dataType === "invalidToken") {
          // トークンがシステムに登録されていないか、
          // もしくは有効期限切れで削除された後である場合
          // 何もしない。（ユーザにパスワード入力してもらう）
        } else {
          throw "invalid data type.";
        }
      };
      this.socket.onclose = (e) => {
        console.log(e);
        // this.initializeWebSocket();
      };
      this.socket.onerror = (e) => {
        console.log(e);
      };
    },
    onClickSubmitButton() {
      if (!this.password) {
        return;
      }
      this.socket.send(
        JSON.stringify({
          action: "sendPassword",
          data: {
            password: this.password,
            userName: this.userName,
          },
        })
      );
    },
  },
  name: "Login",
};
</script>

<style lang="scss" scoped>
#login {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.form-container {
  width: 360px;
  height: 100%;
  padding: 16px;
  background-color: #f0f0f0;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.password-forms {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;
}
.invalid-password-label {
  color: red;
}
</style>
