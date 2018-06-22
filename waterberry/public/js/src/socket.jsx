import io from 'socket.io-client';

let socket = null;

const subscribeToElectrovalveData = cb => {
  socket = io();
  socket.on('connect', () => {
    console.log("connect ...");
  });
  socket.on('data', data => cb(null, data));
}

const unSubscribeToElectrovalveData = () => {
  socket.disconnect()
}

export {
  subscribeToElectrovalveData,
  unSubscribeToElectrovalveData
};
