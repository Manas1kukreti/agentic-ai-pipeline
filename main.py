print(" MAIN FILE STARTED")

from graph import app

print(" GRAPH IMPORTED SUCCESSFULLY")

result = app.invoke({
    "retry_count": 0
})

print(" GRAPH EXECUTION FINISHED")

print("\n FINAL OUTPUT:\n")
print(result)