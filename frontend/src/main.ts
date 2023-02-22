// @ts-ignore
import { createFastboard, mount } from "@netless/fastboard";
// @ts-ignore
import type { FastboardApp } from "@netless/fastboard";
import Cookies from "js-cookie";

const appDiv = <HTMLDivElement>document.getElementById("app");

const appEvent = new EventTarget();
const app = new Proxy<{
  value: FastboardApp | undefined;
}>(
  {
    value: undefined,
  },
  {
    set: function (obj, prop, value) {
      if (prop !== "value") {
        return false;
      }

      obj[prop] = value;
      appEvent.dispatchEvent(new CustomEvent("updated"));
      return true;
    },
  }
);

const createRoom = () => {
  const csrftoken = Cookies.get("csrftoken") || "";
  fetch("/api/create-room", {
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  }).then(async (resp) => {
    if (resp.ok) {
      const config = await resp.json();
      app.value = await createFastboard({
        ...config,
        managerConfig: {
          cursor: true,
        },
      });
      // @ts-ignore
      window.app = app.value;
      mount(app.value, appDiv);
    }
  });
};

const joinRoom = () => {
  const roomId = (<HTMLInputElement>document.getElementById("joinRoomId"))
    .value;
  const csrftoken = Cookies.get("csrftoken") || "";
  fetch("/api/join-room", {
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      roomId,
    }),
  }).then(async (resp) => {
    if (resp.ok) {
      const config = await resp.json();
      app.value = await createFastboard({
        ...config,
        managerConfig: {
          cursor: true,
        },
      });
      // @ts-ignore
      window.app = app.value;

      // @ts-ignore
      const modal = bootstrap.Modal.getOrCreateInstance("#joinRoomModal");
      modal.hide();

      mount(app.value, appDiv);
    }
  });
};

document.getElementById("create_room")!.addEventListener("click", createRoom);
document.getElementById("join_room")!.addEventListener("click", joinRoom);
document
  .getElementById("destory_room_connection")!
  .addEventListener("click", async () => {
    if (app.value) {
      await app.value.destroy();
      app.value = undefined;
      location.reload();
    }
  });

appEvent.addEventListener("updated", () => {
  const roomJoined = document.querySelectorAll(".room_joined");
  const notRoomJoined = document.querySelectorAll(".not_room_joined");

  if (app.value) {
    roomJoined.forEach((elem) => {
      elem.classList.remove("d-none");
    });
    notRoomJoined.forEach((elem) => {
      elem.classList.add("d-none");
    });
  } else {
    roomJoined.forEach((elem) => {
      elem.classList.add("d-none");
    });
    notRoomJoined.forEach((elem) => {
      elem.classList.remove("d-none");
    });
  }
  (<HTMLInputElement>document.getElementById("roomId"))!.value = app.value
    ? app.value.room.uuid
    : "";
});
