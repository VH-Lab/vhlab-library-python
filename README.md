# vhlab-library-python
A python conversion of vhlab-library-matlab

## Installation

To set up a virtual environment for local development:

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Where each function came from

Every `vhlib` package carries a `vhlib_matlab_python_bridge.yaml` that records,
for each function, its MATLAB source in
[vhlab-library-matlab](https://github.com/VH-Lab/vhlab-library-matlab), the
MATLAB revision it was checked against, its argument mapping, and what was
decided along the way — including what is deliberately *not* ported and why.

Start at [`vhlib/vhlib_matlab_python_bridge.yaml`](vhlib/vhlib_matlab_python_bridge.yaml),
which decodes the package-name abbreviations (`CDM` ← `CellDatabaseManagement`,
`md` ← `MeasuredData`, `StimDecode` ← `StimulusDecoding`) and gives a decision
for every area of the MATLAB library. See `PORTING_INSTRUCTIONS` for the
convention.

## Testing

```bash
python3 -m unittest discover -s tests
```
