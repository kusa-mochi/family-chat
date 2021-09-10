<template>
  <div id="login">
    <div v-show="inputLabelVisible" class="input-label">パスワード違うし</div>
    <input v-model="password" placeholder="パスワード" type="password" />
    <button @click="onClickSubmitButton">OK</button>
  </div>
</template>

<script>
export default {
  computed: {
    webSocketUrl: {
      get() {
        return this.$store.state.webSocketUrl;
      },
    },
  },
  created() {
    this.initializeWebSocket();
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
        } else if (parsedData.dataType === "invalidPassword") {
          // パスワードが違った場合
          this.inputLabelVisible = true;
        }
      };
      this.socket.onclose = (e) => {
        console.log(e);
        this.initializeWebSocket();
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
          },
        })
      );
    },
  },
  name: "Login",
};
</script>

<style lang="scss" scoped>
.input-label {
  color: red;
}
</style>
