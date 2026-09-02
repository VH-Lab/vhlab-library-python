# Missing functions from vlt (vhlab-toolbox-python)

The following functions were found to be missing in `vhlab-toolbox-python` but are required by `vhlab-library-python`:

- `string2associates` (likely in `vlt.data`)
- a public .mat reader. `vlt.file.dirstruct._load_mat_file` is exactly what
  `vhlib.StimDecode.getstimscript` and `repairoverflow_stimtimes_txt` need — it
  handles v5/v6/v7 through scipy and v7.3 through h5py — but its leading
  underscore says it is private. Promoting it (or an equivalent) to a public
  name in `vlt.file` would let both callers stop reaching into another
  package's internals.

Note: `findassociate`, `associate`, `disassociate`, `associate_all` are now implemented in `vhlib.md`.
`getpathname`, `gettests`, `saveexpvar`, `getexperimentfile` are available in `vlt.file.dirstruct`.
`loadStructArray` is available in `vlt.file.custom_struct_io`.
`load2celllist` is available in `vlt.file.load2celllist`.
`getstimdirectorytime` is implemented in `vhlib.StimDecode`.
`getstimscript` is implemented in `vhlib.StimDecode` as the free function taking a
directory name, which is the form NDI calls. It is not the same function as
`vlt.file.dirstruct.dirstruct.getstimscript`, which is the dirstruct method.

---

This file records what this repository needs from `vhlab-toolbox-python`. For
the other direction — what this repository takes from `vhlab-library-matlab`,
and what it deliberately leaves behind — see the
`vhlib_matlab_python_bridge.yaml` files described in `PORTING_INSTRUCTIONS`.
`associate_all` in particular is recorded there as a stopgap that belongs in
`vhlab-toolbox-python`.
