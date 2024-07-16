from flask import render_template

def error_404(error):
    return render_template('404.html', error=error)

def error_500(error):
  return render_template('500.html', error=error)