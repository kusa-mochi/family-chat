<template>
  <div id="chat">
    <div class="chat-container">
      <div class="chat-logs">
        <div v-for="item in chatLogs" :key="item.key" class="log-item">
          <div class="log-item__user-name">{{ item.name }}:</div>
          <div class="log-item__message">{{ item.message }}</div>
        </div>
      </div>
      <div class="chat-form-container">
        <input
          v-model="stringToSend"
          @keyup.enter="sendChat"
          class="chat-input"
          placeholder="書きたい文をここに書いてね"
        />
        <button
          @click="sendChat"
          :disabled="!isSendButtonEnabled"
          class="send-button"
          type="button"
        >
          <img class="send-button-icon" src="@/assets/baby.svg" />
        </button>
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
    },
    webSocketUrl: {
      get() {
        return this.$store.state.webSocketUrl;
      },
    },
  },
  created() {
    console.log("creating chat component..");
    if (this.socket === null) {
      this.initializeWebSocket();
    }
  },
  data() {
    return {
      chatLogs: [
        // {
        //   key: 1,
        //   name: "あああああ",
        //   message:
        //     "あんｖｒｂがおｇんｓｇのｇばががおがｇｂｓｇｂｓｂｓｂｓがえお",
        // },
        // {
        //   key: 2,
        //   name: "いいいいいいい",
        //   message: "faegのｖせｒごｓｈごあｒがえがおえがｇなおｇはが",
        // },
      ],
      logKey: 1,
      isSendButtonEnabled: false,
      stringToSend: "",
      socket: null,
    };
  },
  methods: {
    initializeWebSocket() {
      console.log("initializing websocket on chat component..");
      this.socket = new WebSocket(this.webSocketUrl);
      this.socket.onopen = (e) => {
        console.log(e);
        this.socket.send(
          JSON.stringify({
            action: "updateConnectionId",
            data: {
              token: this.token,
            },
          })
        );
      };
      this.socket.onmessage = (e) => {
        const parsedData = JSON.parse(e.data);
        console.log(parsedData);

        if (parsedData.dataType === "receivedChat") {
          console.log("receivedChat");
          // チャットを受信した場合
          new Audio(require("@/assets/sounds/hitsuji.mp3")).play();
          this.chatLogs.unshift({
            key: this.logKey++,
            name: parsedData.data.userName,
            message: parsedData.data.message,
          });
          return;
        } else if (parsedData.dataType === "updatedConnectionId") {
          console.log("updatedConnectionId");
          this.isSendButtonEnabled = true;

          parsedData.data.logs.forEach((log) => {
            this.chatLogs.unshift({
              key: this.logKey++,
              name: log.userName,
              message: log.message,
            });
          });
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
    sendChat() {
      // 文字列をLambdaに送る。
      console.log("sending chat..");
      console.log({
        action: "sendChat",
        data: {
          token: this.token,
          message: this.stringToSend,
        },
      });
      this.socket.send(
        JSON.stringify({
          action: "sendChat",
          data: {
            token: this.token,
            message: this.stringToSend,
          },
        })
      );

      // input要素の文字列をクリアする。
      this.stringToSend = "";
    },
  },
  name: "Chat",
};
</script>

<style lang="scss" scoped>
#chat {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.chat-container {
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
.chat-logs {
  width: 100%;
  height: 500px;
  background-color: transparent;
  border: 1px solid gray;
  margin-bottom: 8px;

  display: flex;
  flex-direction: column-reverse;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;

  .log-item {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: flex-start;

    $userNameWidth: 100px;
    &__user-name {
      width: $userNameWidth;
    }
    &__message {
      width: calc(100% - #{$userNameWidth});
    }
  }
}
.chat-form-container {
  width: 100%;
  height: 24px;

  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;
}
.chat-input {
  width: calc(100% - 32px);
  height: 24px;
}
.send-button {
  width: 32px;
  height: 24px;
}
.send-button-icon {
  height: 24px;
}
</style>
