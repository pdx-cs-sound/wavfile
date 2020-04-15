# wavfile — show WAVE audio file header information
Bart Massey

This utility gives some summary statistics about WAVE
(`.wav`) audio files given as arguments on the command line.

This code requires `numpy` and `soundfile`: use `pip install`
to install if needed.

## To-Do

This is very much a work in progress:

* [x] Allow floating-point soundfiles.
* [ ] Test with 64-bit floating-point soundfile.
* [ ] Test with 24-bit integer soundfile.
* [ ] Allow various non-linear encodings.
* [ ] Test 8-bit integer code.

## License

This utility is made available under the "MIT License". Please see
the file `LICENSE` in this distribution for license terms.
