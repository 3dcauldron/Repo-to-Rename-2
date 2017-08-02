from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        height = request.POST.get('height', 0)
        duration = request.POST.get('duration', 0)
        frequency = request.POST.get('frequency', 0)
        pause = request.POST.get('pause', False)
        beep = request.POST.get('beep', False)
        fs = FileSystemStorage()
        
        filename = fs.save(myfile.name, myfile)
        fname = "/projects/djangoDocker/mediafiles/" + filename
        output = process_gcode_file("/projects/djangoDocker/mediafiles/" + filename, height, duration, frequency, pause, beep)
        f = open(filename,'w')
        f.write(output)
        f.close()
        response = HttpResponse(output, content_type='text/plain')
        rest = filename.split('_', 1)[0]
        
        response['Content-Disposition'] = 'attachment; filename=%s' % rest + "_changed.txt"
        return response
    return render(request, 'gcode/index.html')
    
    
def process_gcode_file(filename, heightInMM, duration, frequency, pause, beep):
    pause_command = 'M600\n'
    beep_command = 'M300 ' + frequency + ' ' + duration + '\n'
    
    f = open(filename).readlines()
    listOfLines = list()
    h = "%s%s" % ("Z", str(heightInMM))
    for line in f:
        listOfLines.append(line)
        if h in line:
            if pause:
                listOfLines.append(beep_command)
                listOfLines.append(pause_command)
            elif beep:
                listOfLines.append(beep_command)
    return ''.join(listOfLines)