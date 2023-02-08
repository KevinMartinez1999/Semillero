import numpy as np

def demapper_sym(symbols_I, symbols_Q, Ns, threshold = 2.0):
   symbol = []
   for i in range(Ns):
        if symbols_I[i] <= -threshold and symbols_Q[i] >= threshold: #-3+3j
            symbol.append(0)
        elif symbols_I[i] <= -threshold and symbols_Q[i] >= 0 and symbols_Q[i] <= threshold: #-3+1j
            symbol.append(1)
        elif symbols_I[i] <= -threshold and symbols_Q[i] <= 0 and symbols_Q[i] >= -threshold: #-3-j
            symbol.append(3)
        elif symbols_I[i] <= -threshold and symbols_Q[i] <= -threshold: #-3-3j
            symbol.append(2)
        elif symbols_I[i] >= -threshold and symbols_I[i] <= 0 and symbols_Q[i] >= threshold: #-1+3j
            symbol.append(4)
        elif symbols_I[i] >= -threshold and symbols_I[i] <= 0 and symbols_Q[i] >= 0 and symbols_Q[i] <= threshold: #-1+j
            symbol.append(5)
        elif symbols_I[i] >= -threshold and symbols_I[i] <= 0 and symbols_Q[i] <= 0 and symbols_Q[i] >= -threshold: #-1-j
            symbol.append(7)
        elif symbols_I[i] >= -threshold and symbols_I[i] <= 0 and symbols_Q[i] <= -threshold: #-1-3j
            symbol.append(6)
        elif symbols_I[i] >= 0 and symbols_I[i] <= threshold and symbols_Q[i] >= threshold: #1+3j
            symbol.append(12)
        elif symbols_I[i] >= 0 and symbols_I[i] <= threshold and symbols_Q[i] >= 0 and symbols_Q[i] <= threshold: #1+j
            symbol.append(13)
        elif symbols_I[i] >= 0 and symbols_I[i] <= threshold and symbols_Q[i] <= 0 and symbols_Q[i] >= -threshold: #1-j
            symbol.append(15)
        elif symbols_I[i] >= 0 and symbols_I[i] <= threshold and symbols_Q[i] <= -threshold: #1-3j
            symbol.append(14)
        elif symbols_I[i] >= threshold and symbols_Q[i] >= threshold: #3+3j
            symbol.append(8)
        elif symbols_I[i] >= threshold and symbols_Q[i] >= 0 and symbols_Q[i] <= threshold: #3+1j
            symbol.append(9)
        elif symbols_I[i] >= threshold and symbols_Q[i] <= 0 and symbols_Q[i] >= -threshold: #3-1j
            symbol.append(11)
        elif symbols_I[i] >= threshold and symbols_Q[i] <= -threshold: #3-3j
            symbol.append(10)
   return(symbol)

def add_noise(arr, noise_db):
    '''
    Adición de ruido blanco Gaussiano (AWGN).
    Se le adiciona diferentes cantidades de ruido para ver los efectos de 
    este en la demodulación. '''

    X_avg_p = np.mean(np.power(arr, 2))
    X_avg_db = 10 * np.log10(X_avg_p)
    noise_avg_db = X_avg_db - noise_db
    noise_avg_p = np.power(10, noise_avg_db / 10)
    mean_noise = 0
    noise = np.random.normal(mean_noise, np.sqrt(noise_avg_p), len(arr))
    return arr + noise

def symbol_error_rate(sym_tx, sym_rx):
  error = 0
  for i, rx in enumerate(sym_rx):
    if rx != sym_tx[i]:
      error += 1
  SER = error / len(sym_tx)
  return SER, error

def bit_error_rate(sym_tx, sym_rx):
  sym_rx_bin = ''.join([f'{sym:04b}' for sym in sym_rx])
  sym_tx_bin = ''.join([f'{sym:04b}' for sym in sym_tx])
  error = 0
  for i in range(len(sym_tx_bin)):
    if sym_rx_bin[i] != sym_tx_bin[i]:
      error += 1
  BER = error / len(sym_tx_bin)
  return BER, error

def sync_signals(trama_tx, trama_rx):
  tx = np.concatenate((trama_tx, trama_tx))
  corr = np.abs(np.correlate(np.abs(tx) - np.mean(np.abs(tx)),
                             np.abs(trama_rx) - np.mean(np.abs(trama_rx)), mode='full'))
  delay = np.argmax(corr) + 1 - len(trama_rx)
  #print(f'El retraso es de {delay} posiciones')
  trama_sync = tx[delay:]
  trama_sync = trama_sync[:len(trama_rx)]
  return trama_sync