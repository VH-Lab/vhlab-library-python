# Missing functions from vlt (vhlab-toolbox-python)

The following functions were found to be missing in `vhlab-toolbox-python` but are required by `vhlab-library-python`:

- `string2associates` (likely in `vlt.data`)

Note: `findassociate`, `associate`, `disassociate`, `associate_all` are now implemented in `vhlib.md`.
`getpathname`, `gettests`, `saveexpvar`, `getexperimentfile` are available in `vlt.file.dirstruct`.
`loadStructArray` is available in `vlt.file.custom_struct_io`.
`load2celllist` is available in `vlt.file.load2celllist`.
`getstimdirectorytime` is implemented in `vhlib.StimDecode`.

---

This file records what this repository needs from `vhlab-toolbox-python`. For
the other direction — what this repository takes from `vhlab-library-matlab`,
and what it deliberately leaves behind — see the
`vhlib_matlab_python_bridge.yaml` files described in `PORTING_INSTRUCTIONS`.
`associate_all` in particular is recorded there as a stopgap that belongs in
`vhlab-toolbox-python`.
