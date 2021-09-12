<template>
  <div id="chat">
    <div class="chat-container">
      <div class="chat-logs">
        <div v-for="item in chatLogs" :key="item.key" class="log-item">
          <div class="log-item__user-name">{{ item.name }}</div>
          <div class="log-item__message">
            <template v-if="isUrl(item.message)">
              <a :href="item.message" target="_blank">{{ item.message }}</a>
            </template>
            <template v-else>
              {{ item.message }}
            </template>
          </div>
        </div>
      </div>
      <div class="chat-form-container">
        <el-form class="chat-form" @submit.native.prevent="sendChat">
          <el-form-item class="chat-form-item">
            <el-input
              ref="chatinput"
              v-model="stringToSend"
              class="chat-input"
              placeholder="書きたい文をここに書いてね"
              ><el-button
                slot="append"
                @click="sendChat"
                :disabled="!isSendButtonEnabled"
                class="send-button"
                ><img
                  class="send-button__icon"
                  src="@/assets/images/baby.png" /></el-button
            ></el-input>
          </el-form-item>
        </el-form>
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

          // ログに追加する。
          this.chatLogs.unshift({
            key: this.logKey++,
            name: parsedData.data.userName,
            message: parsedData.data.message,
          });
          return;
        } else if (parsedData.dataType === "updatedConnectionId") {
          console.log("updatedConnectionId");
          this.isSendButtonEnabled = true;

          // 受信したログの内容で初期化する。
          this.chatLogs.splice(0, this.chatLogs.length);
          let logs = parsedData.data.logs.slice();
          logs.sort(
            (logA, logB) => logA.expirationDatetime - logB.expirationDatetime
          );
          logs.forEach((log) => {
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
    isUrl(s) {
      try {
        new URL(s);
        return true;
      } catch {
        return false;
      }
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
  mounted() {
    this.$refs.chatinput.focus();
  },
  name: "Chat",
};
</script>

<style lang="scss" scoped>
#chat {
  position: relative;
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.chat-container {
  position: relative;
  width: 50%;
  height: 100%;
  padding: 8px;
  background-color: #f0f0f0;

  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
.chat-logs {
  position: relative;
  width: 100%;
  background-color: #fafafa;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  overflow-x: hidden;
  overflow-y: auto;

  display: flex;
  flex-direction: column-reverse;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;

  flex-grow: 1;

  .log-item {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-start;
    align-items: stretch;

    margin: 4px;

    $userNameWidth: 100px;
    &__user-name {
      width: $userNameWidth;
      overflow-wrap: break-word;
      word-break: break-all;
      border-right: 1px solid #169632;
      background-color: rgba(#169632, 0.1);
      padding: 4px;
    }
    &__message {
      width: calc(100% - #{$userNameWidth});
      overflow-wrap: break-word;
      word-break: break-all;
      padding: 4px;
    }
  }
}
.chat-form-container {
  position: relative;
  width: 100%;

  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: flex-start;
}
.chat-form {
  width: 100%;
}
.chat-form-item {
  width: 100%;
  margin: 0;
}
.chat-input {
  width: 100%;
}
.send-button {
  &__icon {
    width: 32px;
  }
}

@media screen and (max-width: 850px) {
  .chat-container {
    width: 70%;
  }
}
@media screen and (max-width: 630px) {
  .chat-container {
    width: 90%;
  }
}
@media screen and (max-width: 500px) {
  .chat-container {
    width: 100%;
    padding: 0;
  }
}
</style>
