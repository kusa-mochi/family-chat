<template>
  <div id="chat">
    <div class="chat-container">
      <div class="chat-logs">
        <div v-for="item in chatLogs" :key="item.key" class="log-item">
          <div class="log-item__user-name">{{ item.name }}</div>
          <div class="log-item__message">{{ item.message }}</div>
        </div>
      </div>
      <div class="chat-form-container">
        <input class="chat-input" placeholder="書きたい文をここに書いてね" />
        <button class="send-button" type="button">
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
      set(newValue) {
        this.$store.state.token = newValue;
      },
    },
    webSocketUrl: {
      get() {
        return this.$store.state.webSocketUrl;
      },
    },
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
      socket: null,
    };
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
