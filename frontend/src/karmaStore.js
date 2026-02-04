let listeners = [];

export function notifyKarmaChanged() {
  listeners.forEach((fn) => fn());
}

export function subscribeKarma(fn) {
  listeners.push(fn);
  return () => {
    listeners = listeners.filter((l) => l !== fn);
  };
}
