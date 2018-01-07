import io from 'socket.io-client';
const socket = io();

socket.on('connect', () => {
  console.log("connect ...");
});

const subscribeToElectrovalveData = cb => {
  socket.on('data', data => cb(null, data));
}

export {
  subscribeToElectrovalveData
};
