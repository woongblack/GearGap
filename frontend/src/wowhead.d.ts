interface WowheadPower {
  init(): void;
}

declare global {
  interface Window {
    $WowheadPower?: WowheadPower;
  }
}

export {};
