# Winform import
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# basic form
$window = New-Object System.Windows.Forms.Form
$window.Text = 'OCTOPY'
$window.Size = '300, 200'

# Labels
    # Header
$header = New-Object System.Windows.Forms.Label
$header.Text = 'OCTOPY - CSOMAGOLÁS'
$header.AutoSize = $false
$header.TextAlign = [System.Drawing.ContentAlignment]::TopCenter
$header.Dock = 'Top'
$window.Controls.Add($header)
    # Footer
$footer = New-Object System.Windows.Forms.Label
$hostname = hostname
$footer.Text = "$hostname"
$footer.AutoSize = $false
$footer.TextAlign = [System.Drawing.ContentAlignment]::BottomCenter
$footer.Dock = 'Bottom'
$window.Controls.Add($footer)

# Buttons
    # Kimutatás másolása
$copyExcelButton = New-Object System.Windows.Forms.Button
$copyExcelButton.Text = 'Kimutatás másolása'
$copyExcelButton.Size = '125, 30'
$copyExcelButton.Location = '10, 30'
$window.Controls.Add($copyExcelButton)
    # Kimutatás megnyitása
$openExcelButton = New-Object System.Windows.Forms.Button
$openExcelButton.Text = 'Kimutatás megnyitása'
$openExcelButton.Size = '125, 30'
$openExcelButton.Location = '145, 30'
$window.Controls.Add($openExcelButton)


# escape on 'ESC' event
$window.Add_KeyDown({
    param($sender, $e)
    if ($e.KeyCode -eq [System.Windows.Forms.Keys]::Escape) {
        $sender.Close()
    }
})

# Show form
$window.ShowDialog()